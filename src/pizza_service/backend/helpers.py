import uuid
from asyncio import sleep

from backend.base import Communication
from db.models import Order
from fastapi.exceptions import HTTPException
from backend.schemas import Pizza
from sqlalchemy.ext.asyncio import AsyncSession
from aiokafka import AIOKafkaProducer


async def add_pizza(db: AsyncSession, order_uuid: str, pizza: dict) -> None:
    if order := await Order.get_by_column(db, column_name="uuid", column_value=order_uuid):
        current_pizzas = order.pizzas
        current_pizzas.append(pizza)
        await Order.update(db, column_name="uuid", column_value=order_uuid, pizzas=current_pizzas)
    return None


async def add_movie_ticket(db: AsyncSession, order_uuid: str, movie_ticket: dict) -> None:
    """
    TODO I assume the problem lies with connection to db.
    raise sa_exc.InvalidRequestError(
    sqlalchemy.exc.InvalidRequestError:
    This session is provisioning a new connection;
    concurrent operations are not permitted (Background on this error at: https://sqlalche.me/e/20/isce)

    TODO I assume the problem lies with connection to db.
    return await Order.update(db, column_name="uuid", column_value=order_uuid, movie_ticket=movie_ticket)
    File "kafka-python-getting-started/src/pizza_service/db/models.py", line 41, in update
    setattr(target_obj, key, value)
    AttributeError: 'NoneType' object has no attribute 'movie_ticket'
    """
    # try:
    print(order_uuid)
    return await Order.update(db, column_name="uuid", column_value=order_uuid, movie_ticket=movie_ticket)
    # except AttributeError:
        # print("Warning: Order hasn't created yet")
        # await sleep(1)
        # await add_movie_ticket(db, order_uuid, movie_ticket)



async def get_order(db: AsyncSession, order_uuid: str) -> dict | HTTPException:
    try:
        return await Order.get_by_column(db, column_name="uuid", column_value=order_uuid)
    except KeyError:
        raise HTTPException(404, f"Order {order_uuid} not found")


async def get_pizza_image() -> dict | None:
    request = Communication("https://foodish-api.com/api/images/pizza")
    data = await request.get_response()
    if isinstance(data, HTTPException):
        return await None
    return data


async def pizza_generation(
    uuid: str,
    schema: Pizza,
    count: int
) -> Pizza:

    for i in range(count):
        pizza = schema()
        pizza.order_id = uuid
        if image_data := await get_pizza_image():
            pizza.image = image_data["image"]
            yield pizza


async def order_pizza(db: AsyncSession, producer: AIOKafkaProducer, count: int):
    """
    create sequence of pizzas by ::count::
    sent each pizza to kafka ingredient consumer
    """
    order = await Order.create(db, uuid=str(uuid.uuid4().int), count=count)

    async for pizza in pizza_generation(order.uuid, Pizza, count):
        await producer.send_and_wait("pizza", key=order.uuid.encode("utf-8"), value=pizza.model_dump_json().encode("utf-8"))
        print(f"Producer sent message!{count}")

    await producer.send_and_wait("order", key=order.uuid.encode("utf-8"), value=b"")
    print("Producer sent all messages!")

    return order.uuid



