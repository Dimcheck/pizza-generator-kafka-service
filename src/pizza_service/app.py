import asyncio
from typing import Any, List

import uvicorn
from backend import schemas
from backend.kafka import service
from db import models
from db.session import DB_DEPENDENCY, get_db
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from templates import pizza_service

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/order/{count}")
async def order_pizzas(
    db: DB_DEPENDENCY,
    count: int,
) -> HTMLResponse:
    """order specific amount of pizzas with random fillings"""

    order = await service.order_pizzas(db, int(count))
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


@app.on_event("startup")
async def launch_consumers():
    async for db in get_db():
        asyncio.create_task(service.load_orders(db))
        asyncio.create_task(service.load_order_bonuses(db))




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
