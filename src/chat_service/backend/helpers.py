import json
from collections.abc import Sequence
from typing import Any

from exceptions import IncorectDataError
from websockets.asyncio.server import ServerConnection


class BroadcastManager:
    def __init__(self, clients: Sequence[ServerConnection]) -> None:
        self.clients = clients

    async def broadcast(self, message: str) -> None:
        """Broadcast user message to all active chat members."""
        for client in self.clients:
            await client.send(message)

    async def broadcast_connection_count(self) -> None:
        """Broadcast the current connection count to all active chat members."""
        await self.broadcast(
            json.dumps(
                {
                    "type": "connection_count",
                    "count": len(self.clients),
                },
            ),
        )

    async def broadcast_message(self, message: Any, websocket: ServerConnection) -> None:
        """validate message and broadcast it."""
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
