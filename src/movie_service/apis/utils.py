import os
from random import random
from pathlib import Path
from configparser import ConfigParser

ENV_PATH = str(list(Path(__file__).parents)[1] / "configs" / ".env")


def read_env():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value


def make_config(pathfile: str = "config.properties") -> dict:
    config_parser = ConfigParser()
    config_parser.read(pathfile)
    return dict(config_parser["kafka_client"])


def with_chance(chance: float = 0.1):
    """
    should be used with functions
    where invokation supposed to be random to degree
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if random() < chance:
                return func(*args, **kwargs)
        return wrapper
    return decorator

