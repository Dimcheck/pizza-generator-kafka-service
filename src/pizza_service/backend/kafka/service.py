import json

from backend.helpers import add_movie_ticket, add_pizza
from backend.kafka.objects import Pizza, PizzaOrder
from backend.pizza_img_api import get_pizza_image
from backend.utils import make_config
from confluent_kafka import Consumer, Producer


orders_db = {}
current_config = make_config()


def order_pizzas(count: int) -> str:
    """
    create sequence of pizzas by ::count::
    sent each pizza to kafka ingredient consumer
    """
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
    """
    accept last ingredient from pizza-with-veggies kafka producer
    add pizza to order
    """
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
            add_pizza(pizza["order_id"], pizza, orders_db)


def load_order_bonuses() -> None:
    """
    accept bonuses (if there are any) after order creation
    add bonuses to order
    """
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
            add_movie_ticket(event.key().decode("ascii"), movie_ticket, orders_db)

