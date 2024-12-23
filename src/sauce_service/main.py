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


async def add_sauce(order_id: str, pizza: dict) -> None:
    sauce_producer = AIOKafkaProducer(**current_config["producer"])
    pizza["sauce"] = random.choice(
        [
            'regular', 'light', 'extra',
            'none', 'alfredo', 'regular',
            'light', 'extra', 'alfredo',
        ]
    )
    await sauce_producer.start()
    try:
        await sauce_producer.send_and_wait("pizza-with-sauce", key=order_id.encode("utf-8"), value=json.dumps(pizza).encode("utf-8"))
    finally:
        await sauce_producer.stop()


async def start_service():
    pizza_consumer = AIOKafkaConsumer(**current_config["consumer"])
    pizza_consumer.subscribe(["pizza"])

    await pizza_consumer.start()
    try:
        async for event in pizza_consumer:
            if event is not None:
                print("Caught event from PizzaGenerator PRODUCER")
                pizza = json.loads(event.value.decode("utf-8"))
                await add_sauce(event.key.decode("utf-8"), pizza)
    finally:
        await pizza_consumer.stop()


if __name__ == "__main__":
    asyncio.run(start_service())

