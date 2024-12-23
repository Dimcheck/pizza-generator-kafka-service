import json
import os
from pathlib import Path
from configparser import ConfigParser


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
    consumer_config1 = dict(config_parser["consumer1"])
    consumer_config2 = dict(config_parser["consumer2"])

    return {
        "producer": producer_config,
        "consumer1": consumer_config1,
        "consumer2": consumer_config2,
    }


def encode_serializer(message):
    return json.dumps(message).encode('utf-8')


def decode_serializer(message):
    try:
        return json.loads(message.decode('utf-8'))
    except json.JSONDecodeError:
        if isinstance(message, bytes):
            return message.decode('utf-8')
        else:
            return message
