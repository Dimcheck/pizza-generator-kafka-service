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


def add_meat(order_id: str, pizza: dict) -> None:
    meat_producer = Producer(current_config)
    pizza["meats"] = " & ".join(
        random.choices(
            [
                'anchovies', 'salami',  'bacon',
                'pepperoni', 'sausage', 'ham',
            ],
            k=random.randint(1, 6)
        )
    )
    meat_producer.produce("pizza-with-meats", key=order_id, value=json.dumps(pizza))
    meat_producer.flush()


def start_service():
    pizza_consumer = Consumer(current_config)
    pizza_consumer.subscribe(["pizza-with-cheese"])

    while True:
        event = pizza_consumer.poll(1.0)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_meat(event.key(), pizza)


if __name__ == "__main__":
    start_service()

