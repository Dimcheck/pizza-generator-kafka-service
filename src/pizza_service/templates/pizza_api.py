import json

from fastapi.responses import HTMLResponse
from kafka import service


def list_pizzas(order_id: str) -> HTMLResponse:
    order = service.orders_db[order_id]
    pizzas = json.loads(order["_PizzaOrder__pizzas"])

    html_content = f"""
    <body>
        <p>Pizzas:</p>
        <h3>{order.get("id", "")}</h3>
        <table border="1" style="width: 100%; border-collapse: collapse;">
            <tr>
                <th>Sauce</th>
                <th>Cheese</th>
                <th>Meats</th>
                <th>Veggies</th>
                <th>Image</th>
            </tr>
    """

    for pizza in pizzas:
        html_content += f"""
            <tr>
                <td>{pizza["sauce"]}</td>
                <td>{pizza["cheese"]}</td></tr>
                <td>{pizza["meats"]}</td></tr>
                <td>{pizza["veggies"]}</td></tr>
                <img src="{pizza.get("image")} alt="pizza img"/>
            </tr>
        """

    html_content += """
        </table>
    </body>
    """

    return HTMLResponse(content=html_content, status_code=200)


