from backend.helpers import FRONTEND_DIR
from backend.routes import router
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR / "static")), name="static")
app.include_router(router)


