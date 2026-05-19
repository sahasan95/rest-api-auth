from pydantic import BaseModel, EmailStr, ConfigDict

# 1. Base properties shared across schemas
class UserBase(BaseModel):
    email: EmailStr

# 2. Properties expected when creating a new user (Registration)
class UserCreate(UserBase):
    password: str

# 3. Properties returned back to the client/frontend safely
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    # Pydantic v2 configuration to read data directly from database objects
    model_config = ConfigDict(from_attributes=True)