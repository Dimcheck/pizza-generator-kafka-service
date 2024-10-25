from dataclasses import dataclass
import json
import uuid


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
    order_id: str
    sauce: str
    cheese: str
    meats: str
    veggies: str


class PizzaOrder(SerializableMixin):
    def __init__(self, count):
        self.id = str(uuid.uuid4().int)
        self.count = count
        self.pizzas = []

    @property
    def pizzas(self):
        return self.__pizzas

    @pizzas.setter
    def add_pizza(self, pizza: dict):
        self.pizzas.append(pizza)

    def get_pizzas(self):
        return self.pizzas



