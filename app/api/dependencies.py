from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.settings import get_settings
from app.db.session import get_db
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
async def current_user(token:str=Depends(oauth2_scheme),db:AsyncSession=Depends(get_db)):
    try: return jwt.decode(token,get_settings().jwt_secret_key,algorithms=[get_settings().jwt_algorithm])
    except JWTError as exc: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token") from exc

def require_roles(*roles):
    async def dependency(user=Depends(current_user)):
        if user.get("role") not in roles and user.get("is_admin") is not True:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Insufficient role")
        return user
    return dependency
