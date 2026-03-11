from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.shemas.user import UserCreate

async def get_user_by_email(db : AsyncSession, email : str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def get_user_by_id(db : AsyncSession, user_id : int) -> User | None:
    result = await db.execute(select(User).where(User.id == id))
    return result.scalar_one_or_none()

async def create_user(db : AsyncSession, data : UserCreate) -> User:
    user = User(
        email = data.email,
        username = data.username,
        hashed_password = get_password_hash(data.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)
    return user

async def authenticate_user(db : AsyncSession, email : str, password : str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user