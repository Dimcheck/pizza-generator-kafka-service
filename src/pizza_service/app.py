from threading import Thread

import uvicorn
from backend.kafka import service
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
def order_pizzas(count) -> HTMLResponse:
    """order specific amount of pizzas with random fillings"""
    return pizza_service.list_order(service.order_pizzas(int(count)))


@app.get("/orders/")
def get_all_orders():
    return service.orders_db


@app.get("/order/{order_id}")
def get_order(order_id):
    return pizza_service.list_pizzas(order_id)


@app.get("/order_bonus/{order_id}")
def get_order_bonuses(order_id):
    return pizza_service.check_movie_ticket(order_id)


@app.on_event("startup")
def launch_consumers():
    second_thread = Thread(target=service.load_orders)
    third_thread = Thread(target=service.load_order_bonuses)

    second_thread.start()
    third_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
