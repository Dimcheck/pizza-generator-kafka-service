import os
from pathlib import Path

ENV_PATH = str(list(Path(__file__).parents)[1] / "configs" / ".env")


def read_env():
    with open(ENV_PATH) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=", 1)
                os.environ[key] = value



