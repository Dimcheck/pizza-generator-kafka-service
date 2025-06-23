## About
Supposed to be a support/general popup chat on main page of pizza service.

## Setup

1. Run everything with fastapi
```bash
poetry run uvicorn backend.fa_ws_server:app --reload --port 8000
```

2. **Optionally:** run websocket interactive client
```bash
poetry run python -m websockets ws://localhost:8000/ws
```

>**Deprecated**
>1. Run ws server
>```bash
>poetry run python -m backend.ws_server
>```
>2. Run http server
>```bash
>poetry run python -m http.server 8000
>```


## Usage
Join [chat](http://127.0.0.1:8000) and have fun!