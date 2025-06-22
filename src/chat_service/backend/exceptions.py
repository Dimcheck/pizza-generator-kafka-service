import json

from websockets.asyncio.server import ServerConnection


class WebsocketError(Exception):
    message: str = ""
    
    def __init__(self, websocket: ServerConnection) -> None:
        self.websocket = websocket
        super().__init__(self.message)
    
    async def send(self) -> None:
        await self.websocket.send(
            json.dumps(
                {
                    "type": "error",
                    "text": self.message,
                },
            ),
        )
 
class IncorectDataError(WebsocketError):
    message = "You've tried to send incorrect data"
    

