import json
from threading import Thread

import service
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from templates import movie_api

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/order/{count}")
def order_pizzas(count):
    """order specific amount of pizzas with random fillings"""
    order_id = service.order_pizzas(int(count))
    return HTMLResponse(content=json.dumps({"order_id": order_id}), status_code=200)


@app.get("/orders/")
def get_all_orders():
    return HTMLResponse(content=service.orders_db, status_code=200)


@app.get("/order/{order_id}")
def get_order(order_id):
    return service.get_order(order_id)


@app.get("/movie/", response_class=HTMLResponse)
def get_movie_html(movie_name: str) -> HTMLResponse:
    """get accostomed with htmx endpoints flow"""
    return HTMLResponse(content=movie_api.short_desc(movie_name), status_code=200)


# @app.on_event("startup")
def launch_consumer():
    second_thread = Thread(target=service.load_orders)
    second_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
