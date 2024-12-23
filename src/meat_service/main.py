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


async def add_meat(order_id: str, pizza: dict) -> None:
    meat_producer = AIOKafkaProducer(**current_config["producer"])
    pizza["meats"] = " & ".join(
        random.choices(
            [
                'anchovies', 'salami',  'bacon',
                'pepperoni', 'sausage', 'ham',
            ],
            k=random.randint(1, 6)
        )
    )
    await meat_producer.start()
    try:
        await meat_producer.send_and_wait("pizza-with-meats", key=order_id.encode("utf-8"), value=json.dumps(pizza).encode("utf-8"))
    finally:
        await meat_producer.stop()


async def start_service():
    pizza_consumer = AIOKafkaConsumer(**current_config["consumer"])
    pizza_consumer.subscribe(["pizza-with-cheese"])

    await pizza_consumer.start()
    try:
        async for event in pizza_consumer:
            if event is not None:
                print("Consumer caught event!")
                pizza = json.loads(event.value.decode("utf-8"))
                await add_meat(event.key.decode("utf-8"), pizza)
    finally:
        await pizza_consumer.stop()


if __name__ == "__main__":
    asyncio.run(start_service())

