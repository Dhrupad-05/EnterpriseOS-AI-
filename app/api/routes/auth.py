from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.auth import LoginRequest, TokenResponse
from app.db.session import get_db
from app.models.entities import User
from app.core.security import create_access_token, create_refresh_token, verify_password
router=APIRouter(prefix="/auth",tags=["Authentication"])
@router.post("/login",response_model=TokenResponse)
async def login(data:LoginRequest,db:AsyncSession=Depends(get_db)):
    user=(await db.execute(select(User).where(User.email==data.email,User.is_active.is_(True),User.is_deleted.is_(False)))).scalar_one_or_none()
    if not user or not verify_password(data.password,user.password_hash): raise HTTPException(status_code=401,detail="Invalid credentials")
    return TokenResponse(access_token=create_access_token(str(user.id)),refresh_token=create_refresh_token(str(user.id)))
