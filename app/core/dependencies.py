from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import decode_token
from app.db.session import get_db
from app.models.user import User
from app.services.auth import get_user_by_id

bearer_scheme = HTTPBearer()

async def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(bearer_scheme),
        db : AsyncSession = Depends(get_db),
) -> User:
    payload = decode_token(credentials.credentials)
    
    if payload is None:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid or expired token",
        )
    
    user = await get_user_by_id(db, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user