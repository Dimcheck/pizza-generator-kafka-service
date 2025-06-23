import json

from fastapi import WebSocket
from websockets.asyncio.server import ServerConnection


class WebsocketError(Exception):
    message: str = ""
    
    def __init__(self, websocket: ServerConnection | WebSocket) -> None:
        self.websocket = websocket
        self.data = json.dumps({"type": "error", "text": self.message})
        super().__init__(self.message)
    
    async def send(self) -> None:
        
        if isinstance(self.websocket, WebSocket):
            await self.websocket.send_text(self.data)
        else:    
            await self.websocket.send(self.data)
    
class IncorectDataError(WebsocketError):
    message = "You've tried to send incorrect data"
    

