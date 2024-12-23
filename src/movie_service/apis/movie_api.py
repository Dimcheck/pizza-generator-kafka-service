import os
from random import randint

from apis.base import Communication
from apis.utils import read_env

read_env()
OMDB_KEY = os.environ.get("OMDB_KEY")


def get_movie(movie_name: str = "") -> dict:
    request = Communication("https://www.omdbapi.com")
    return request.get_response_with_params(apikey=OMDB_KEY, t=movie_name)


def get_random_movie() -> dict:
    imdb_id = str(randint(1, 9000000))
    while len(imdb_id) <= 6:
        imdb_id = "0" + imdb_id

    request = Communication("https://www.omdbapi.com")
    return request.get_response_with_params(apikey=OMDB_KEY, i=f"tt{imdb_id}")
