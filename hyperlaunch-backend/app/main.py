from fastapi import FastAPI
from app.api.routes import router as api_router
from app.core.config import settings
from app.core.logger import setup_logging
from app.core.db import init_db

setup_logging()

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="0.1.0",
    description="Base FastAPI boilerplate with clean structure"
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(api_router, prefix="/api")

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "FastAPI is running!"}
