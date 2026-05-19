from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import user as crud_user
from app.schemas import user as user_schemas
from app.db.session import get_db
from app.core import security

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=user_schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: user_schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Registers a new user account if the email address is unique.
    """
    # 1. Check if a user with this email address already exists
    existing_user = await crud_user.get_user_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email address already exists."
        )
    
    # 2. Create and return the user
    new_user = await crud_user.create_user(db, user_in=user_in)
    return new_user


@router.post("/login", response_model=user_schemas.Token)
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticates a user and returns an OAuth2-compatible JWT access token.
    """
    # 1. Look up user by their username (email)
    user = await crud_user.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Generate and return the secure JWT token
    access_token = security.create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}