import os
from dataclasses import dataclass
from datetime import timedelta
from backend.utils import read_env

read_env()


@dataclass
class Settings:
    ACCESS_TOKEN_EXPIRE:  timedelta = timedelta(minutes=15)
    REFRESH_TOKEN_EXPIRE: timedelta = timedelta(days=1)
    API_V1_STR:           str = "/api/v1"
    PROJECT_NAME:         str = "Pizza-Generator-Service"

    MYSQL_USER:        str = os.getenv("MYSQL_USER")
    MYSQL_PASSWORD:    str = os.getenv("MYSQL_PASSWORD")
    MYSQL_DB:          str = os.getenv("MYSQL_DB")
    MYSQL_PORT:        int = os.getenv("MYSQL_PORT", 6024)
    MYSQL_SERVER:      str = os.getenv("MYSQL_SERVER")

    DATABASE_URL:         str = f"mysql+aiomysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"


settings = Settings()
