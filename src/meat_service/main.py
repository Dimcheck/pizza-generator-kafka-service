from configparser import ConfigParser
from confluent_kafka import Producer, Consumer
import json
import random


def make_config(pathfile: str = "config.properties") -> dict:
    config_parser = ConfigParser(interpolation=None)
    with open(pathfile, "r") as config:
        config_parser.read(config)
        return config_parser["kafka_client"]


current_config = make_config()


def add_meat(order_id: int, pizza: dict) -> None:
    sauce_producer = Producer(current_config)
    pizza["meats"] = random.choice(
        [
            'pepperoni', 'sausage', 'ham',
            'anchovies', 'salami', 'bacon',
            'pepperoni', 'sausage', 'ham',
            'anchovies', 'salami', 'bacon'
        ]
    )
    sauce_producer.produce("pizza-with-meats", key=order_id, value=json.dumps(pizza))


def start_service():
    pizza_consumer = Consumer(current_config)
    pizza_consumer.subscribe(["pizza-with-cheese"])

    while True:
        event = pizza_consumer.poll(0.1)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_meat(event.key(), pizza)


if __name__ == "__main__":
    start_service()

