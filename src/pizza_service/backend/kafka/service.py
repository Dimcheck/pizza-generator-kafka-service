import asyncio
import json
import uuid

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from backend.helpers import add_movie_ticket, add_pizza, get_pizza_image
from backend.schemas import Pizza
from backend.utils import make_config
from db.models import Order
from sqlalchemy.ext.asyncio import AsyncSession

current_config = make_config()


async def order_pizzas(db: AsyncSession, count: int) -> str:
    """
    create sequence of pizzas by ::count::
    sent each pizza to kafka ingredient consumer
    """
    main_producer = AIOKafkaProducer(**current_config["producer"])

    await main_producer.start()

    order_uuid = str(uuid.uuid4().int)
    order = await Order.create(db, uuid=order_uuid, count=count)

    for i in range(count):
        new_pizza = Pizza()
        new_pizza.order_id = order.uuid
        image_data = await get_pizza_image()
        new_pizza.image = image_data["image"]
        print(f"image {i} loaded from {count}..")
        print(new_pizza)
        await main_producer.send_and_wait("pizza", key=order.uuid.encode("utf-8"), value=new_pizza.model_dump_json().encode("utf-8"))
        print("Producer sent messages!")

    try:
        await main_producer.send_and_wait("order", key=order.uuid.encode("utf-8"), value=b"")
        print("Producer sent all messages!")
    finally:
        await main_producer.stop()

    return order.uuid


async def load_orders(db: AsyncSession) -> None:
    """
    accept last ingredient from pizza-with-veggies kafka producer
    add pizza to order
    """
    # pizza_consumer = AIOKafkaConsumer(*["pizza-with-veggies"], **current_config["consumer1"])
    pizza_consumer = AIOKafkaConsumer(**current_config["consumer1"])
    await pizza_consumer.start()
    pizza_consumer.subscribe(["pizza-with-veggies"])
    print("Consumer started!")

    async for event in pizza_consumer:
        if event is None:
            ...
        else:
            pizza = json.loads(event.value.decode("utf-8"))
            print("Caught event from VEGGIES PRODUCER")
            await add_pizza(db, pizza["order_id"], pizza)


async def load_order_bonuses(db: AsyncSession) -> None:
    """
    accept bonuses (if there are any) after order creation
    add bonuses to order
    """
    # order_consumer = AIOKafkaConsumer(*["movie-ticket"], **current_config["consumer2"])
    order_consumer = AIOKafkaConsumer(**current_config["consumer2"])
    await order_consumer.start()
    order_consumer.subscribe(["movie-ticket"])
    print("Consumer started!")

    async for event in order_consumer:
        if event is None:
            ...
        else:
            movie_ticket = json.loads(event.value.decode("utf-8"))
            print("Caught event from ORDER PRODUCER")
            await add_movie_ticket(db, event.key.decode("utf-8"), movie_ticket)

