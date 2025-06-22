## About
Supposed to be a support/general popup chat on main page of pizza service.

## Setup
1. Run ws server
```bash
python backend/ws_server.py
```
2. Run http server
```bash
python -m http.server 8000
```

>**Optionally:** run websocket interactive client
>```bash
>python -m websockets ws://localhost:8001/
>```

## Usage
Join [chat](http://127.0.0.1:8000/frontend/) and have fun!