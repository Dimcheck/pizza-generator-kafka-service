from fastapi import FastAPI

app = FastAPI()
pizzas = []


@app.get("/")
def read_root():
    return "yo"


@app.post("/order/{pizza_id}")
def generate_first_layer(pizza_id: int):
    ...
