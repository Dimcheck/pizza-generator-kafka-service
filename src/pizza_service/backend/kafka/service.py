import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from backend.helpers import add_movie_ticket, add_pizza


async def startup_producer(producer: AIOKafkaProducer) -> AIOKafkaProducer:
    await producer.start()
    return producer


async def startup_consumer1(consumer: AIOKafkaConsumer) -> None:
    """
    accept last ingredient from pizza-with-veggies kafka producer
    add pizza to order
    """
    consumer.subscribe(["pizza-with-veggies"])
    print("Consumer started!")

    await consumer.start()
    try:
        async for event in consumer:
            if event is not None:
                pizza = json.loads(event.value.decode("utf-8"))
                print("Caught event from VEGGIES PRODUCER")
                await add_pizza(pizza["order_id"], pizza)
    finally:
        await consumer.stop()


async def startup_consumer2(consumer: AIOKafkaConsumer) -> None:
    """
    accept bonuses (if there are any) after order creation
    add bonuses to order
    """
    consumer.subscribe(["movie-ticket"])
    print("Consumer started!")

    await consumer.start()
    try:
        async for event in consumer:
            if event is not None:
                if movie_ticket := json.loads(event.value.decode("utf-8")):
                    print("Caught event from ORDER PRODUCER")
                    await add_movie_ticket(event.key.decode("utf-8"), movie_ticket)
    finally:
        await consumer.stop()

