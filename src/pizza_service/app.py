import asyncio
import uvicorn

from typing import Any, List
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from backend import schemas
from backend.helpers import order_pizza
from backend.utils import make_config, encode_serializer, decode_serializer
from backend.kafka import service
from templates import pizza_service
from db import models
from db.session import DB_DEPENDENCY

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

current_config = make_config()


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

loop = asyncio.get_event_loop()
producer = AIOKafkaProducer(
    **current_config["producer"],
    # key_serializer=encode_serializer,
    # value_serializer=encode_serializer,
    loop=loop
)
consumer1 = AIOKafkaConsumer(
    **current_config["consumer1"],
    # key_serializer=decode_serializer,
    # value_deserializer=decode_serializer,
    loop=loop
)
consumer2 = AIOKafkaConsumer(
    **current_config["consumer2"],
    # key_serializer=decode_serializer,
    # value_deserializer=decode_serializer,
    loop=loop
)


@app.on_event("startup")
async def startup():
    await service.startup_producer(producer)
    loop.create_task(service.startup_consumer1(consumer1))
    loop.create_task(service.startup_consumer2(consumer2))


@app.on_event("shutdown")
async def shutdown():
    await producer.stop()
    await consumer1.stop()
    await consumer2.stop()


@app.post("/order/{count}")
async def order_pizzas(
    db: DB_DEPENDENCY,
    count: int,
) -> HTMLResponse:
    """order specific amount of pizzas with random fillings"""

    order = await order_pizza(db, producer, int(count))
    return await pizza_service.list_order(order)


@app.get("/orders/", response_model=List[schemas.Order])
async def get_all_orders(
    db: DB_DEPENDENCY,
) -> Any:

    return await models.Order.get_all(db)


@app.get("/order/{order_uuid}")
async def get_order(
    db: DB_DEPENDENCY,
    order_uuid: str,
) -> HTMLResponse:

    return await pizza_service.list_pizzas(db, order_uuid)


@app.get("/order_bonus/{order_uuid}")
async def get_order_bonuses(
    db: DB_DEPENDENCY,
    order_uuid: str,
) -> HTMLResponse:

    return await pizza_service.check_movie_ticket(db, order_uuid)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
