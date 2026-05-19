from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A foundational REST API featuring robust asynchronous JWT authentication.",
    version="1.0.0"
)

@app.get("/", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }