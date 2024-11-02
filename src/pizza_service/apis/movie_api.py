import os

from apis.utils import read_env
from apis.base import Communication

read_env()
OMDB_KEY = os.environ.get("OMDB_KEY")


"""
:TODO: include logic to win tickets for random movie
:TODO: make separate service from it
"""

def get_movie(movie_name: str = "") -> dict:
    request = Communication("https://www.omdbapi.com")
    return request.get_response_with_params(apikey=OMDB_KEY, t=movie_name)

