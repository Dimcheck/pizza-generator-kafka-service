import json
from configparser import ConfigParser
from pathlib import Path

from confluent_kafka import Consumer, Producer
from objects import Pizza, PizzaOrder

CONFIG_PATH = str(Path(__file__).parent / "configs/config.properties",)


def make_config(pathfile: str) -> dict:
    config_parser = ConfigParser()
    config_parser.read(pathfile)
    producer_config = dict(config_parser["kafka_client"])
    consumer_config = dict(config_parser["kafka_client"])
    consumer_config.update(config_parser["consumer"])
    return {"producer": producer_config, "consumer": consumer_config}


orders_db = {}
current_config = make_config(CONFIG_PATH)


def order_pizzas(count: int) -> int:
    pizza_producer = Producer(current_config["producer"])
    order = PizzaOrder(count)
    orders_db[order.id] = order

    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        pizza_producer.produce("pizza", key=order.id, value=new_pizza.to_json())

    pizza_producer.flush()
    return order.id


def add_pizza(order_id: str, pizza: dict) -> None:
    if order_id in orders_db.keys():
        order = orders_db[order_id]
        order.add_pizza(pizza)


def get_order(order_id: str) -> str:
    order = orders_db[order_id]
    if order is None:
        return "Order not found, maybe it's not ready yet"
    else:
        return order.to_json()


def load_orders() -> None:
    pizza_consumer = Consumer(current_config["consumer"])
    pizza_consumer.subscribe(["pizza-with-veggies"])

    while True:
        event = pizza_consumer.poll(1.0)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            pizza = json.loads(event.value())
            add_pizza(pizza["order_id"], pizza)

