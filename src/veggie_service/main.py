import asyncio
import json
import random
from configparser import ConfigParser
from pathlib import Path

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

CONFIG_PATH = str(Path(__file__).parent / "config.properties",)


def make_config(pathfile: str = "config.properties") -> dict:
    config_parser = ConfigParser()
    config_parser.read(pathfile)
    producer_config = dict(config_parser["kafka_client"])
    consumer_config = dict(config_parser["consumer"])
    return {
        "producer": producer_config,
        "consumer": consumer_config,
    }


current_config = make_config(CONFIG_PATH)


async def add_veggie(order_id: str, pizza: dict) -> None:
    veggie_producer = AIOKafkaProducer(**current_config["producer"])
    await veggie_producer.start()

    pizza["veggies"] = " & ".join(
        random.choices(
            [
                'tomato',  'olives', 'onions',
                'peppers', 'pineapple', 'mushrooms',
            ],
            k=random.randint(1, 6)
        )
    )
    try:
        await veggie_producer.send_and_wait("pizza-with-veggies", key=order_id.encode("utf-8"), value=json.dumps(pizza).encode("utf-8"))
    finally:
        await veggie_producer.stop()


async def start_service():
    # pizza_consumer = AIOKafkaConsumer(*["pizza-with-meats"], **current_config["consumer"])
    pizza_consumer = AIOKafkaConsumer(**current_config["consumer"])
    await pizza_consumer.start()
    pizza_consumer.subscribe(["pizza-with-meats"])

    async for event in pizza_consumer:
        if event is None:
            ...
        else:
            pizza = json.loads(event.value.decode("utf-8"))
            await add_veggie(event.key.decode("utf-8"), pizza)


if __name__ == "__main__":
    asyncio.run(start_service())

