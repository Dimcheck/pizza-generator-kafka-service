from fastapi.responses import HTMLResponse
from fastapi.exceptions import HTTPException
from kafka import service


def list_pizzas(order_id: str) -> HTMLResponse:
    try:
        order = service.orders_db[order_id].__dict__
    except KeyError:
        raise HTTPException(404, f"Order {order_id} not found")
    pizzas = order["_PizzaOrder__pizzas"]

    html_content = f"""
    <body>
        <h3>Pizzas of order #{order.get("id", "")}</h3>
    """
    for pizza in pizzas:
        html_content += f"""
        <ul>
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


