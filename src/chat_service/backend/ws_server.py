import asyncio
import json
from websockets.asyncio.server import serve


clients = set()


async def handler(websocket):
    clients.add(websocket)
    # Send a welcome message to the new client
    await websocket.send(json.dumps({
        "type": "message",
        "username": "Server",
        "text": "Welcome to the chat!"
    }))

    async for message in websocket:
        data = json.loads(message)
        if data["type"] == "message":
            broadcast = json.dumps({
                "type": "message",
                "username": data["username"],
                "text": data["text"]
            })

            for client in clients:
                await client.send(broadcast)


async def main():
    async with serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())