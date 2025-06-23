import json
from typing import Set

from backend.helpers import FRONTEND_DIR, BroadcastManager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")
connections: Set[WebSocket] = set()

with open(FRONTEND_DIR / "index.html", "r") as f:
    html_content = f.read()

@app.get("/")
async def get() -> HTMLResponse:
    """Serve the chat HTML page"""
    return HTMLResponse(content=html_content)

async def broadcast_message(message: str, sender: WebSocket = None) -> None:
    """Broadcast a message to all connected connections"""
    for connection in connections:
        if connection != sender:  # Don't send back to the sender
            await connection.send_text(message)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Handle WebSocket connections"""
    await websocket.accept()
    connections.add(websocket)
    bm = BroadcastManager(connections)

    await websocket.send_text(
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
        while True:
            message = await websocket.receive_text()
            await bm.broadcast_message(message, websocket)
    except WebSocketDisconnect:
        connections.remove(websocket)
        await bm.broadcast_connection_count()