from fastapi import FastAPI
from app.core.config import settings
from app.api.routes.webhook import router as webhook_router

app = FastAPI(title=settings.app_name)

@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.app_name, "env": settings.app_env}

app.include_router(webhook_router)