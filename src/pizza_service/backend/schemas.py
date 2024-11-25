from pydantic import BaseModel
from typing import List


class Pizza(BaseModel):
    order_id: str = ''
    sauce: str = ''
    cheese: str = ''
    meats: str = ''
    veggies: str = ''
    image: str = ''


class Order(BaseModel):
    uuid: str
    count: int
    pizzas: List[Pizza]
    movie_ticket: dict
