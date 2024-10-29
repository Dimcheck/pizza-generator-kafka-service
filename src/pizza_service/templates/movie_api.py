from apis import movie_api
from fastapi.responses import HTMLResponse


def short_desc(movie_name: str = "") -> str:
    movie_data = movie_api.get_movie(movie_name)
    html_content = f"""
        <body>
            <h3>{movie_data.get("Title", "Movie Title")}</h3>
            <img src={movie_data.get("Poster", "Movie Poster")} alt="movie-poster"/>
            <p>About:</p>
            <ul>
                <li>Genre: {movie_data.get("Genre", "Genre")}</li>
                <li>imdbRating: {movie_data.get("imdbRating", "Rating")}</li>
                <li>Actors: {movie_data.get("Actors", "Actors")}</li>
            </ul>
            {movie_data.get("Plot", "Movie Plot")}
        </body>
    """
    return HTMLResponse(content=html_content, status_code=200)
