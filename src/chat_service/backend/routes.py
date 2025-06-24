import asyncio
from typing import Set

from backend.helpers import (
    BroadcastManager,
    ShutdownManager,
    WebSocketData,
)
from backend.settings import html_content, logger
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

connections: Set[WebSocket] = set()
shutdown_manager = ShutdownManager(connections, logger, 100)

router = APIRouter(on_startup=[shutdown_manager.startup_event])

@router.get("/")
async def get() -> HTMLResponse:
    """Serve the chat HTML page"""
    return HTMLResponse(content=html_content)

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Handle WebSocket connections"""
    lock = asyncio.Lock()
    if shutdown_manager.is_shutting_down:
        ...
    else:
        await websocket.accept()
        async with lock:
            connections.add(websocket)
        bm = BroadcastManager(connections, logger)
        try:
            await websocket.send_text(
                WebSocketData(
                    text="Welcome to the chat!",
                ).model_dump_json(exclude_none=True),
            )
            await bm.broadcast_connection_count()
            
            while True:
                message = await websocket.receive_text()
                await bm.broadcast_message(message, websocket)
        except WebSocketDisconnect:
            logger.info("Client disconnected normally")
        except Exception as e:
            logger.warning("WebSocket error: %s", e)
        finally:
            if websocket in connections:
                async with lock:
                    connections.remove(websocket)
                if not shutdown_manager.is_shutting_down:
                    await bm.broadcast_connection_count()
                logger.debug("Client disconnected. Remaining connections: %d", {len(connections)})