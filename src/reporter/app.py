from fastapi import FastAPI
from threading import Thread
import service
import uvicorn


app = FastAPI(__name__)


@app.get("/report")
def read_root():
    return service.generate_report()


@app.on_event("startup")
def launch_consumer():
    second_thread = Thread(target=service.start_consumer)
    second_thread.start()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8010, reload=True)
