from asyncio import sleep

from backend.base import Communication
from db.models import Order
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def add_pizza(db: AsyncSession, order_uuid: str, pizza: dict) -> None:
    if order := await Order.get_by_column(db, column_name="uuid", column_value=order_uuid):
        current_pizzas = order.pizzas or []
        current_pizzas.append(pizza)
        await Order.update(db, column_name="uuid", column_value=order_uuid, pizzas=current_pizzas)
    return None



async def add_movie_ticket(db: AsyncSession, order_uuid: str, movie_ticket: dict) -> None:
    for i in range(3):
        try:
            await Order.update(db, column_name="uuid", column_value=order_uuid, movie_ticket=movie_ticket)
        except Exception:
            print("Warning: Order have not created yet")
            await sleep(1)


async def get_order(db: AsyncSession, order_uuid: str) -> dict | HTTPException:
    try:
        return Order.get_by_column(db, column_name="uuid", column_value=order_uuid)
    except KeyError:
        raise HTTPException(404, f"Order {order_uuid} not found")


async def get_pizza_image() -> dict:
    request = Communication("https://foodish-api.com/api/images/pizza")
    return await request.get_response()
