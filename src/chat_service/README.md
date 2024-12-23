## About
Supposed to be a support/general popup chat on main page of pizza service.

## Setup

Prepare webpage
```
python -m http.server
```
Run ws server
```
python backend/ws_server
```
Run websocket interactive client
```
python -m websockets ws://localhost:8001/
```

