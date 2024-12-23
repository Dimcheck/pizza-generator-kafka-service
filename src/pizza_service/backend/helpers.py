import uuid

from aiokafka import AIOKafkaProducer
from backend.base import Communication
from backend.schemas import Pizza
from db.models import Order
from db.session import get_db
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def add_pizza(order_uuid: str, pizza: dict) -> None:
    async for db in get_db():
        if order := await Order.get_by_column(db, column_name="uuid", column_value=order_uuid):
            current_pizzas = order.pizzas
            current_pizzas.append(pizza)
            await Order.update(db, column_name="uuid", column_value=order_uuid, pizzas=current_pizzas)
        return None


async def add_movie_ticket(order_uuid: str, movie_ticket: dict) -> None:
    async for db in get_db():
        return await Order.update(db, column_name="uuid", column_value=order_uuid, movie_ticket=movie_ticket)


async def get_order(db: AsyncSession, order_uuid: str) -> dict | HTTPException:
    try:
        return await Order.get_by_column(db, column_name="uuid", column_value=order_uuid)
    except KeyError:
        raise HTTPException(404, f"Order {order_uuid} not found")


async def get_pizza_image() -> dict | None:
    request = Communication("https://foodish-api.com/api/images/pizza")
    try:
        data = await request.get_response()
    except HTTPException:
        return None
    return data


async def pizza_generation(
    uuid: str,
    schema: Pizza,
    count: int
) -> Pizza | None:

    for i in range(count):
        pizza = schema()
        pizza.order_id = uuid
        if image_data := await get_pizza_image():
            pizza.image = image_data["image"]
            yield pizza


async def order_pizza(db: AsyncSession, producer: AIOKafkaProducer, count: int) -> str:
    """
    create sequence of pizzas by ::count::
    sent each pizza to kafka ingredient consumer
    """
    order = await Order.create(db, uuid=str(uuid.uuid4().int), count=count)

    async for pizza in pizza_generation(order.uuid, Pizza, count):
        await producer.send_and_wait("pizza", key=order.uuid.encode("utf-8"), value=pizza.model_dump_json().encode("utf-8"))
        print("Producer sent message!")

    await producer.send_and_wait("order", key=order.uuid.encode("utf-8"), value=b"")
    print("Producer sent all messages!")

    return order.uuid



