import os
import urllib.request as u_request
import urllib.error as u_error
from fastapi.exceptions import HTTPException
from helpers.utils import read_env


read_env()
OMDB_KEY = os.environ.get("OMDB_KEY")


def get_movie(movie_name: str = ''):
    try:
        with u_request.urlopen(
            f'https://www.omdbapi.com/?apikey={OMDB_KEY}&t={movie_name}'
        ) as response:
            data = response.read()
            return data
    except u_error.HTTPError as e:
        raise HTTPException(e.code, e.reason)
    except u_error.URLError as e:
        raise HTTPException(e.code, e.reason)


