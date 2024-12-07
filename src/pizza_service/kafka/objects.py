import json
import uuid
from dataclasses import dataclass


class SerializableMixin:
    def to_json(self):
        return json.dumps(
            obj=self,
            default=lambda o: o.__dict__,
            sort_keys=False,
            indent=4
        )

    def __str__(self):
        return json.dumps(self.__dict__)


@dataclass
class Pizza(SerializableMixin):
    order_id: str = ''
    sauce: str = ''
    cheese: str = ''
    meats: str = ''
    veggies: str = ''
    image: str = ''


class PizzaOrder(SerializableMixin):
    def __init__(self, count):
        self.id = str(uuid.uuid4().int)
        self.count = count
        self.__pizzas = []
        self.movie_ticket = {}  # TODO add logic for 10% chance of getting a ticket

    @property
    def pizzas(self):
        return self.__pizzas

    def add_pizza(self, pizza: dict):
        self.pizzas.append(pizza)




