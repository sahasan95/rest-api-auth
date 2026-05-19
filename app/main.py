from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.db.base_class import Base

# EXPLICITLY IMPORT MODELS HERE SO BASE DETECTS THEM
from app.models.user import User 

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A foundational REST API featuring robust asynchronous JWT authentication.",
    version="1.0.0"
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }