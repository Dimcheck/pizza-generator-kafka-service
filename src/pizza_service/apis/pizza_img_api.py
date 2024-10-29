from apis.base import Communication


def get_pizza_image() -> dict:
    request = Communication("https://foodish-api.com/api/images/pizza")
    return request.get_response()

