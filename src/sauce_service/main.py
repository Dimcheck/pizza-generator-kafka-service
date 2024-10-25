import json
import random
from configparser import ConfigParser
from pathlib import Path

from confluent_kafka import Consumer, Producer

CONFIG_PATH = str(Path(__file__).parent / "config.properties",)


def make_config(pathfile: str = "config.properties") -> dict:
    config_parser = ConfigParser()
    config_parser.read(pathfile)
    return dict(config_parser["kafka_client"])


current_config = make_config(CONFIG_PATH)


def add_sauce(order_id: str, pizza: dict) -> None:
    sauce_producer = Producer(current_config)
    pizza["sauce"] = random.choice(
        [
            'regular', 'light', 'extra',
            'none', 'alfredo', 'regular',
            'light', 'extra', 'alfredo',
        ]
    )
    sauce_producer.produce("pizza-with-sauce", key=order_id, value=json.dumps(pizza))


def start_service():
    pizza_consumer = Consumer(current_config)
    pizza_consumer.subscribe(["pizza"])

    while True:
        event = pizza_consumer.poll(0.1)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_sauce(event.key(), pizza)


if __name__ == "__main__":
    start_service()

