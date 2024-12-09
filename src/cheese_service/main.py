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


def add_cheese(order_id: str, pizza: dict) -> None:
    cheese_producer = Producer(current_config)
    pizza["cheese"] = random.choice(
        [
            'none', 'ukr cheese', 'goat cheese',
            'extra', 'three cheese',
        ],
    )
    cheese_producer.produce("pizza-with-cheese", key=order_id, value=json.dumps(pizza))
    cheese_producer.flush()


def start_service():
    pizza_consumer = Consumer(current_config)
    pizza_consumer.subscribe(["pizza-with-sauce"])

    while True:
        event = pizza_consumer.poll(1.0)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_cheese(event.key(), pizza)


if __name__ == "__main__":
    start_service()

