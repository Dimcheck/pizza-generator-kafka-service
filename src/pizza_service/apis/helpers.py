from time import sleep


def add_pizza(order_id: str, pizza: dict, db: dict) -> None:
    if order_id in db.keys():
        order = db[order_id]
        order.add_pizza(pizza)


def add_movie_ticket(order_id: str, movie_ticket: dict, db: dict) -> None:
    for i in range(3):
        try:
            db[order_id].movie_ticket = movie_ticket
        except KeyError:
            print("Warning: Order have not created yet")
            sleep(1)


