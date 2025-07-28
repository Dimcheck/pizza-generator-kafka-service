## About
Supposed to be a support/general popup chat on main page of pizza service.

## Setup
1. Create Poetry environment
```bash
# If you want this just for this project and not globally use --local flag
poetry config virtualenvs.in-project true
```
2. install deps
```bash
poetry install
```
3. Run everything with fastapi
```bash
poetry run uvicorn backend.fa_ws_server:app --reload --port 8000
```

>**Optionally:** run websocket interactive client
>```bash
>poetry run python -m websockets ws://localhost:8000/ws
>```
>Send JSON messages in this format:
>```json
>{"type": "message", "username": "YourName", "text": "Your message"}
>```

## Testing WebSocket Endpoint
1. Browser Testing:
  - Join [chat](http://127.0.0.1:8000)!
  - The chat interface will automatically connect to the WebSocket
  - Open multiple browser tabs to simulate different users

2. Using Browser Developer Tools:
  - Open your browser's developer console (F12)
  - In the Network tab, filter by "WS" to monitor WebSocket traffic
  - You can inspect message payloads and connection status

## Graceful Shutdown Logic
The chat service implements a robust graceful shutdown mechanism:

    - The application captures standard termination signals (SIGINT, SIGTERM)
    - When a signal is received, the shutdown process begins without immediately terminating
  
    - All connected clients receive a message: "Server is shutting down for maintenance. Please reconnect later."
    - New connection attempts during shutdown are rejected
  
    - The server attempts to close all WebSocket connections with status code 1000 (normal closure)
    - Connections are continuously monitored during the shutdown process
  
    - A configurable timeout (default: 30 minutes) ensures the server eventually shuts down
    - The server logs remaining connections and time left during shutdown
    - If connections remain after the timeout, the server performs a forced shutdown
  
This approach ensures that:
- Clients receive proper notification before disconnection
- In-flight messages have a chance to complete
- The server eventually terminates even if some connections cannot be closed gracefully

## TODO: Multi-Worker Support with Redis Pub/Sub
The current implementation has a limitation: when running multiple Uvicorn workers (using `--workers` flag), each worker maintains its own separate connection pool and state. This means:

- Messages sent to one worker aren't broadcast to clients connected to other workers
- Connection counts are incorrect as they only reflect connections to a single worker
- Graceful shutdown only affects connections on the worker receiving the signal

A Redis Pub/Sub implementation would:
1. Allow all workers to share a global connection registry
2. Enable cross-worker message broadcasting
3. Provide accurate total connection counts across workers
4. Support coordinated graceful shutdown


