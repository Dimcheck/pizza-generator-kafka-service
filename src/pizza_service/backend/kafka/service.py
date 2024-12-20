import asyncio
import json
import uuid

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from backend.helpers import (
    add_movie_ticket,
    add_pizza,
    pizza_generation,
)
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
    await main_producer.stop()
    await main_producer.start()

    order = await Order.create(db, uuid=str(uuid.uuid4().int), count=count)

    async for pizza in pizza_generation(order, Pizza, count):
        await main_producer.send_and_wait("pizza", key=order.uuid.encode("utf-8"), value=pizza.model_dump_json().encode("utf-8"))
        print("Producer sent messages!")

    await main_producer.send_and_wait("order", key=order.uuid.encode("utf-8"), value=b"")
    print("Producer sent all messages!")

    return order.uuid


async def load_orders(db: AsyncSession) -> None:
    """
    accept last ingredient from pizza-with-veggies kafka producer
    add pizza to order
    """
    pizza_consumer = AIOKafkaConsumer(**current_config["consumer1"])
    await pizza_consumer.start()

    while not await pizza_consumer.topics():
        print("Waiting for topic 'pizza-with-veggies' to be available...")
        await asyncio.sleep(2)

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
    order_consumer = AIOKafkaConsumer(**current_config["consumer2"])
    await order_consumer.start()

    while not await order_consumer.topics():
        print("Waiting for topic 'movie-ticket' to be available...")
        await asyncio.sleep(2)

    order_consumer.subscribe(["movie-ticket"])
    print("Consumer started!")

    async for event in order_consumer:
        if event is None:
            ...
        else:
            movie_ticket = json.loads(event.value.decode("utf-8"))
            print("Caught event from ORDER PRODUCER")
            await add_movie_ticket(db, event.key.decode("utf-8"), movie_ticket)

