import asyncio
import contextlib
import json
import logging
import signal
import sys
import time
from asyncio.tasks import Task
from collections.abc import Set
from copy import copy
from typing import Any, Optional

from backend.exceptions import IncorectDataError
from fastapi import WebSocket
from pydantic import BaseModel
from uvicorn.server import HANDLED_SIGNALS
from websockets.asyncio.server import ServerConnection


class WebSocketData(BaseModel):
    type: str = "message"
    username: str = "Server"
    text: Optional[str] = None
    count: Optional[int] = None


class BroadcastManager:
    def __init__(
        self, 
        connections: Set[ServerConnection | WebSocket], 
        logger: logging.Logger,
    ) -> None:
        self.connections = connections
        self.logger = logger
        self.lock = asyncio.Lock()

    async def broadcast(self, message: str, websocket: Optional[ServerConnection | WebSocket] = None) -> None:
        """Broadcast user message to all active chat members."""
        async with self.lock:
            for connection in self.connections: 
                if connection != websocket:  # Don't send back to the sender
                    try:
                        if isinstance(connection, WebSocket):
                            await connection.send_text(message)
                        else:
                            await connection.send(message)
                    except Exception as e:
                        self.logger.debug("Failed to send message to a connection: %s", e)
                        continue
        
    async def broadcast_connection_count(self) -> None:
        """Broadcast the current connection count to all active chat members."""
        await self.broadcast(
            WebSocketData(
                type="connection_count", count=len(self.connections),
            ).model_dump_json(exclude_unset=True),
        )
    
    async def broadcast_message(self, message: Any, websocket: ServerConnection | WebSocket) -> None:
        """Validate message and broadcast it."""
        try:
            data = json.loads(message)
        except json.JSONDecodeError:
            error = IncorectDataError(websocket)
            return await error.send()
        try:
            content = WebSocketData(username=data["username"], text=data["text"]).model_dump_json(exclude_none=True)
        except KeyError:
            error = IncorectDataError(websocket)
            return await error.send()
            
        return await self.broadcast(content)


class ShutdownManager:
    """Manages graceful shutdown of the application."""
    def __init__(
        self, 
        connections: Set[WebSocket | ServerConnection], 
        logger: logging.Logger,
        max_shutdown_time: int = 30 * 60,
    ) -> None:
        self.connections = connections
        self.MAX_SHUTDOWN_TIME = max_shutdown_time
        self.is_shutting_down = False
        self.worker_id = id(asyncio.current_task()) if asyncio.current_task() else None
        self.logger = logger
        self.lock = asyncio.Lock()
        
    async def monitor_shutdown(self) -> None:
        """Monitor the shutdown process and force shutdown if needed"""
        shutdown_deadline = time.time() + self.MAX_SHUTDOWN_TIME
        async with self.lock:
            while self.connections and time.time() < shutdown_deadline:
                remaining_time = int(shutdown_deadline - time.time())
                remaining_minutes, remaining_seconds = remaining_time // 60, remaining_time % 60
                self.logger.info("Graceful shutdown in progress. Connections remaining: %d", len(self.connections))
                self.logger.info("Time remaining: %d m %d s", remaining_minutes, remaining_seconds)
                for connection in copy(self.connections):
                    with contextlib.suppress(RuntimeError):
                        await connection.close(code=1000, reason="Server shutting down")
                        self.connections.remove(connection)
            if self.connections:
                sys.exit("Time is up. Forcefull shutdown in progress..")
            self.logger.info("All connections closed gracefully")

    async def begin_shutdown(self) -> Task[Any]:
        """Begin the shutdown process"""
        self.is_shutting_down = True
        bm = BroadcastManager(self.connections, self.logger)
        await bm.broadcast(
            WebSocketData(
                text="Server is shutting down for maintenance. Please reconnect later.",
            ).model_dump_json(exclude_none=True),
        )
        return asyncio.create_task(self.monitor_shutdown())
        
    def signal_handler(self, signum: int, frame: Any) -> Task[Any]:
        """Handle shutdown signals"""
        self.logger.info("Received signal %d Starting graceful shutdown...", signum) 
        return asyncio.create_task(self.begin_shutdown())

    async def startup_event(self) -> None:
        """Configure signal handlers for graceful shutdown"""
        for sig in HANDLED_SIGNALS:
            signal.signal(sig, self.signal_handler)
        self.logger.info("Server started. Worker ID: %d ", self.worker_id)
        
