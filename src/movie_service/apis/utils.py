import os
from configparser import ConfigParser
from pathlib import Path
from random import random

ENV_PATH = str(list(Path(__file__).parents)[1] / "configs" / ".env")
CONFIG_PATH = str(Path(__file__).parents[1] / "configs/config.properties",)


def read_env():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value


def make_config(pathfile: str = CONFIG_PATH) -> dict:
    config_parser = ConfigParser()
    config_parser.read(pathfile)
    producer_config = dict(config_parser["kafka_client"])
    consumer_config = dict(config_parser["consumer"])
    return {
        "producer": producer_config,
        "consumer": consumer_config,
    }


def with_chance(chance: float = 0.1):
    """
    should be used with functions
    where invokation supposed to be random to degree
    """
    def decorator(func):
        async def wrapper(*args, **kwargs):
            if random() < chance:
                return await func(*args, **kwargs)
        return wrapper
    return decorator

