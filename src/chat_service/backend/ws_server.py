import asyncio
import json

from helpers import BroadcastManager
from websockets.asyncio.server import ServerConnection, serve

clients = set()


async def handler(websocket: ServerConnection) -> None:
    clients.add(websocket)
    bm = BroadcastManager(clients)
    
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
        clients.remove(websocket)
        await bm.broadcast_connection_count()
        


async def main() -> None:
    async with serve(handler, "", 8001):
        await asyncio.Future() 


if __name__ == "__main__":
    asyncio.run(main())