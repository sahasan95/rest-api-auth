from fastapi import FastAPI, Depends, HTTPException, status
from app.core.config import settings
from app.db.session import engine, get_db  # Imported your real get_db directly!
from app.db.base_class import Base
from app.models.user import User 
from app.models.project import Project  # Ensure you created this file in app/models/project.py

from app.api.v1.auth import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from typing import List
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# 1. Single unified FastAPI initialization using your real config settings
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A foundational REST API featuring robust asynchronous JWT authentication.",
    version="1.0.0"
)

# 2. CORS security allowed origins
origins = [
    "http://localhost:5173",  
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            
    allow_credentials=True,
    allow_methods=["*"],              
    allow_headers=["*"],              
)

# 3. Dynamic Database Schemas
class ProjectSchema(BaseModel):
    id: int
    title: str
    tech_stack: str
    status: str

    class Config:
        from_attributes = True  # Crucial! Allows Pydantic to read live SQLAlchemy rows

class ProjectCreateSchema(BaseModel):
    title: str
    tech_stack: str
    status: str

# Set tokenUrl path to exactly match your prefix path below
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# 4. Startup Database Table Sync Execution
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # This scans your models and automatically maps tables inside auth_app.db
        await conn.run_sync(Base.metadata.create_all)

# 5. Core API Application Routers
app.include_router(auth_router, prefix="/api/v1")


# 6. Secure Projects Endpoint - GET (Fetch From Database)
@app.get("/api/v1/projects", response_model=List[ProjectSchema], tags=["Data Entities"])
async def get_secure_projects(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Evaluates incoming bearer token from Vue client, then queries
    auth_app.db asynchronously to return all active project rows.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session signature missing or invalid."
        )
    
    # Modern async query execution
    result = await db.execute(select(Project))
    db_projects = result.scalars().all()
    return db_projects


# 7. Secure Projects Endpoint - POST (Write To Database)
@app.post("/api/v1/projects", response_model=ProjectSchema, status_code=status.HTTP_201_CREATED, tags=["Data Entities"])
async def create_new_project(
    project_in: ProjectCreateSchema,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    """
    Protected Endpoint: Receives a project payload, verifies authorization,
    and commits a new entry asynchronously directly into the SQL table.
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session signature invalid."
        )
        
    new_project = Project(
        title=project_in.title,
        tech_stack=project_in.tech_stack,
        status=project_in.status
    )
    
    db.add(new_project)
    await db.commit()
    await db.refresh(new_project)
    return new_project


# 8. Root Server Health Status Check
@app.get("/", tags=["Health Check"])
async def health_check():
    return {
        "status": "healthy",
        "project": settings.PROJECT_NAME,
        "version": "1.0.0"
    }