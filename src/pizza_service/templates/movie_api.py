from apis import movie_api


def short_desc(movie_name: str = "") -> str:
    movie_data = movie_api.get_movie(movie_name)
    return f"""
        <body>
            <h3>{movie_data.get("Title", "Movie Title")}</h3>
            <img src={movie_data.get("Poster", "Movie Poster")} alt="movie-poster"/>
            <p>About:</p>
            <ul>
                <li>Genre: {movie_data.get("Genre", "Genre")}</li>
                <li>imdbRating: {movie_data.get("imdbRating", "Rating")}</li>
                <li>Actors: {movie_data.get("Actors", "Actors")}</li>
                <li>{movie_data.get("Genre", "Movie Genre")}</li>
            </ul>
            {movie_data.get("Plot", "Movie Plot")}
        </body>
    """
