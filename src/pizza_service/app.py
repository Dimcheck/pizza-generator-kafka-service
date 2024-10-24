import json
from fastapi import FastAPI
import uvicorn
from src.pizza_service import service
from threading import Thread

app = FastAPI(__name__)


@app.post("/order/{count}")
def order_pizzas(count):
    """order specific amount of pizzas with random fillings"""
    order_id = service.order_pizzas(int(count))
    return json.dumps({"order_id": order_id})


@app.get("/order/{order_id}")
def get_order(order_id):
    return service.get_order(order_id)


@app.on_event("startup")
def launch_consumer():
    second_thread = Thread(target=service.load_orders)
    second_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
