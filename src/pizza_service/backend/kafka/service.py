import json
import uuid

from backend.helpers import add_movie_ticket, add_pizza, get_pizza_image
from backend.schemas import Pizza
from backend.utils import make_config
from confluent_kafka import Consumer, Producer
from db.models import Order
from sqlalchemy.ext.asyncio import AsyncSession

current_config = make_config()


async def order_pizzas(db: AsyncSession, count: int) -> str:
    """
    create sequence of pizzas by ::count::
    sent each pizza to kafka ingredient consumer
    """
    pizza_producer = Producer(current_config["producer"])
    order_producer = Producer(current_config["producer"])

    order_uuid = str(uuid.uuid4().int)
    order = await Order.create(db, uuid=order_uuid, count=count)
    # order = await Order.get_by_column(db, column_name="uuid", column_value=order_uuid)

    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.uuid
        image_data = await get_pizza_image()
        new_pizza.image = image_data["image"]
        print(f"image {i} loaded from {count}..")
        pizza_producer.produce("pizza", key=order.uuid, value=new_pizza.model_dump_json())
    pizza_producer.flush()

    order_producer.produce("order", key=order.uuid, value="")
    order_producer.flush()

    return order.uuid


async def load_orders(db: AsyncSession) -> None:
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
            # TypeError: AsyncSession.execute() missing 1 required positional argument: 'statement
            await add_pizza(db, pizza["order_id"], pizza)



async def load_order_bonuses(db: AsyncSession) -> None:
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
            await add_movie_ticket(db, event.key().decode("ascii"), movie_ticket)

