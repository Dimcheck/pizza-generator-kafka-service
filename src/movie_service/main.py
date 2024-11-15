import json
from pathlib import Path

from apis.movie_api import get_random_movie
from apis.utils import make_config, with_chance
from confluent_kafka import Consumer, Producer

CONFIG_PATH = str(Path(__file__).parent / "configs/config.properties",)
current_config = make_config(CONFIG_PATH)


@with_chance(0.3)
def movie_ticket_producer(order_id: str) -> None:
    ticket_producer = Producer(current_config)
    ticket_producer.produce("movie-ticket", key=order_id, value=json.dumps(get_random_movie()))
    ticket_producer.flush()


def start_service():
    order_consumer = Consumer(current_config)
    order_consumer.subscribe(["order"])

    while True:
        event = order_consumer.poll(1.0)
        if event is None:
            ...
        elif event.error():
            print(f"ERROR: {event.error()}")
        else:
            movie_ticket_producer(event.key())


if __name__ == "__main__":
    start_service()

