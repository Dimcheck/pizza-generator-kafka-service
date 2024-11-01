import json
from time import sleep
from pathlib import Path

from apis.pizza_img_api import get_pizza_image
from apis.utils import make_config
from confluent_kafka import Consumer, Producer
from kafka.objects import Pizza, PizzaOrder

CONFIG_PATH = str(Path(__file__).parents[1] / "configs/config.properties",)


orders_db = {}
current_config = make_config(CONFIG_PATH)


def add_pizza(order_id: str, pizza: dict) -> None:
    if order_id in orders_db.keys():
        order = orders_db[order_id]
        order.add_pizza(pizza)


def add_movie_ticket(order_id: str, movie_ticket: dict) -> None:
    for i in range(3):
        try:
            orders_db[order_id].movie_ticket = movie_ticket
        except KeyError:
            print("Warning: Order have not created yet")
            sleep(1)


def order_pizzas(count: int) -> int:
    pizza_producer = Producer(current_config["producer"])
    order_producer = Producer(current_config["producer"])

    order = PizzaOrder(count)
    orders_db[order.id] = order

    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.id
        new_pizza.image = get_pizza_image()["image"]
        print(f"image {i} loaded from {count}..")
        pizza_producer.produce("pizza", key=order.id, value=new_pizza.to_json())
    pizza_producer.flush()

    order_producer.produce("order", key=order.id, value="")
    order_producer.flush()

    return order.id


def load_orders() -> None:
    pizza_consumer = Consumer(current_config["consumer1"])
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


def load_order_bonuses() -> None:
    order_consumer = Consumer(current_config["consumer2"])
    order_consumer.subscribe(["movie-ticket"])

    while True:
        event = order_consumer.poll(1.0)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            movie_ticket = json.loads(event.value())
            add_movie_ticket(event.key().decode("ascii"), movie_ticket)

