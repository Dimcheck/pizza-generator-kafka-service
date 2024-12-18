import asyncio
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from apis.movie_api import get_random_movie
from apis.utils import make_config, with_chance

current_config = make_config()


@with_chance(0.3)
async def movie_ticket_producer(order_id: str) -> None:
    ticket_producer = AIOKafkaProducer(**current_config["producer"])
    await ticket_producer.start()

    try:
        await ticket_producer.send_and_wait("movie-ticket", key=order_id.encode("utf-8"), value=json.dumps(get_random_movie()).encode("utf-8"))
    finally:
        await ticket_producer.stop()


async def start_service():
    order_consumer = AIOKafkaConsumer(**current_config["consumer"])
    await order_consumer.start()
    order_consumer.subscribe(["order"])

    try:
        async for event in order_consumer:
            if event is None or event.key is None:
                print("skipping empty event")
            else:
                print(event.key)
                await movie_ticket_producer(event.key.decode("utf-8"))
    finally:
        await order_consumer.stop()


if __name__ == "__main__":
    asyncio.run(start_service())

