import json
from threading import Thread

import service
import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.post("/order/{count}")
def order_pizzas(count):
    """order specific amount of pizzas with random fillings"""
    order_id = service.order_pizzas(int(count))
    return json.dumps({"order_id": order_id})


@app.get("/orders/")
def get_all_orders():
    return service.orders_db


@app.get("/order/{order_id}")
def get_order(order_id):
    return service.get_order(order_id)


@app.on_event("startup")
def launch_consumer():
    second_thread = Thread(target=service.load_orders)
    second_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
