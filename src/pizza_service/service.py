import json

from src.pizza_service.objects import Pizza, PizzaOrder
from configparser import ConfigParser
from confluent_kafka import Producer, Consumer


def make_config(pathfile: str = "config.properties") -> dict:
    config_parser = ConfigParser(interpolation=None)
    with open(pathfile, "r") as config:
        config_parser.read(config)
        producer_config, consumer_config = dict(config_parser["kafka_client"]), dict(config_parser["kafka_client"])
        consumer_config.update(config_parser["consumer"])
        return {"producer": producer_config, "consumer": consumer_config}


pizza_warmer = {}
current_config = make_config()


def order_pizzas(count: int) -> int:
    pizza_producer = Producer(current_config["producer"])
    order = PizzaOrder(count)
    pizza_warmer[order.id] = order

    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        pizza_producer.produce("pizza", key=order.id, value=new_pizza.to_json())

    pizza_producer.flush()
    return order.id


def add_pizza(order_id: int, pizza: dict) -> None:
    if order_id in pizza_warmer.keys():
        order = pizza_warmer[order_id]
        order.add_pizza(pizza)


def get_order(order_id: int) -> str:
    order = pizza_warmer[order_id]
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


