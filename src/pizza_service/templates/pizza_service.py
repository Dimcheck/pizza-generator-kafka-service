from backend.helpers import get_order
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession


async def list_order(order_uuid: int) -> HTMLResponse:
    html_content = f"""<span class="fade-in">{order_uuid}</span>"""
    return HTMLResponse(content=html_content, status_code=200)


async def check_movie_ticket(db: AsyncSession, order_uuid: str) -> HTMLResponse:
    order = await get_order(db, order_uuid)
    movie = order.movie_ticket

    if movie.get("Response") == "True":
        html_content = f"""
        You won free ticket to {movie.get("Title")}!
        <ul class="fade-in">
            <li><img src="{movie.get("Poster")}" alt="movie img" style="width: 60px; height: auto;"/></li>
            <li>Genre: {movie.get("Genre")}</li>
            <li>Director: {movie.get("Director")}</li>
            <li>Plot: {movie.get("Plot")}</li>
        </ul>
        """
        return HTMLResponse(content=html_content, status_code=200)
    return HTMLResponse(content="", status_code=404)


async def list_pizzas(db: AsyncSession, order_uuid: str) -> HTMLResponse:
    order = await get_order(db, order_uuid)
    pizzas = order.pizzas

    html_content = f"""
    <body>
        <h3>Pizzas of order #{order.uuid}</h3>
    """
    for pizza in pizzas:
        html_content += f"""
        <ul class="fade-in">
            <li><img src="{pizza.get("image")}" alt="pizza img" style="width: 60px; height: auto;"/></li>
            <li>Sauce: {pizza["sauce"]}</li>
            <li>Cheese: {pizza["cheese"]}</li>
            <li>Meats: {pizza["meats"]}</li>
            <li>Veggies: {pizza["veggies"]}</li>
        </ul>
        """
    html_content += """
        </table>
    </body>
    """
    return HTMLResponse(content=html_content, status_code=200)


