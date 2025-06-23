import asyncio
import json
from collections.abc import Set

from backend.helpers import BroadcastManager
from websockets.asyncio.server import ServerConnection, serve

connections: Set[ServerConnection] = set()


async def handler(websocket: ServerConnection) -> None:
    connections.add(websocket)
    bm = BroadcastManager(connections)
    
    await websocket.send(
        json.dumps(
            {
                "type": "message",
                "username": "Server",
                "text": "Welcome to the chat!",
            },
        ),
    )
    await bm.broadcast_connection_count()
    try:
        async for message in websocket:
            await bm.broadcast_message(message, websocket)
    finally:
        connections.remove(websocket)
        await bm.broadcast_connection_count()
        


async def main() -> None:
    async with serve(handler, "", 8001):
        await asyncio.Future() 


if __name__ == "__main__":
    asyncio.run(main())