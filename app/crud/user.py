from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Queries the database asynchronously to find a user by their email address.
    Returns the User object if found, otherwise returns None.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """
    Creates a new user record in the database. 
    Hashes the plain-text password automatically before saving.
    """
    # 1. Hash the incoming plain text password securely
    hashed_password = get_password_hash(user_in.password)
    
    # 2. Map the Pydantic schema data to our SQLAlchemy Model structure
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        is_active=True,
        is_superuser=False
    )
    
    # 3. Add to the database session pipeline and commit the transaction
    db.add(db_user)
    await db.commit()
    
    # 4. Refresh our local object to pull database-generated data (like the new auto-increment ID)
    await db.refresh(db_user)
    return db_user