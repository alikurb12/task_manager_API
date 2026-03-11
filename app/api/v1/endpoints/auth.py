from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.shemas.token import Token
from app.shemas.user import UserCreate, UserLogin, UserRead
from app.services.auth import authenticate_user, create_user, get_user_by_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(
    data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    if await get_user_by_email(db, data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )
    return await create_user(db, data)