import json
from collections.abc import Set
from pathlib import Path
from typing import Any, Optional

from backend.exceptions import IncorectDataError
from fastapi import WebSocket
from websockets.asyncio.server import ServerConnection

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

class BroadcastManager:
    def __init__(self, connections: Set[ServerConnection | WebSocket]) -> None:
        self.connections = connections

    async def broadcast(self, message: str, websocket: Optional[ServerConnection | WebSocket] = None) -> None:
        """Broadcast user message to all active chat members."""
        for connection in self.connections:
            if connection != websocket:  # Don't send back to the sender
                if isinstance(connection, WebSocket):
                    await connection.send_text(message)
                else:
                    await connection.send(message)

    async def broadcast_connection_count(self) -> None:
        """Broadcast the current connection count to all active chat members."""
        await self.broadcast(json.dumps({"type": "connection_count", "count": len(self.connections)}))

    async def broadcast_message(self, message: Any, websocket: ServerConnection | WebSocket) -> None:
        """Validate message and broadcast it."""
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            error = IncorectDataError(websocket)
            return await error.send()
        try:
            content = json.dumps({
                "type": "message",
                "username": data["username"],
                "text": data["text"],
            })
        except KeyError:
            error = IncorectDataError(websocket)
            return await error.send()
            
        return await self.broadcast(content)
