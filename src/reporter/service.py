import json

from configparser import ConfigParser
from confluent_kafka import Consumer


def make_config(pathfile: str = "config.properties") -> dict:
    config_parser = ConfigParser(interpolation=None)
    with open(pathfile, "r") as config:
        config_parser.read(config)
        producer_config, consumer_config = dict(config_parser["kafka_client"]), dict(config_parser["kafka_client"])
        consumer_config.update(config_parser["consumer"])
        return {"producer": producer_config, "consumer": consumer_config}


pizzas_with_cheeses_db = {}
current_config = make_config()


def add_cheese(cheese: dict) -> None:
    if cheese in pizzas_with_cheeses_db:
        pizzas_with_cheeses_db[cheese] = pizzas_with_cheeses_db[cheese] + 1
    else:
        pizzas_with_cheeses_db[cheese] = 1


def start_consumer() -> None:
    """
    Supposed to be run in parallel with pizza generator
    to keep count of pizzas with cheese.
    """
    pizza_consumer = Consumer(current_config["consumer"])
    pizza_consumer.subscribe(["pizza-with-cheese"])

    while True:
        event = pizza_consumer.poll(1.0)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_cheese(pizza["cheese"])


def generate_report():
    return json.dumps(pizzas_with_cheeses_db, indent=4)
