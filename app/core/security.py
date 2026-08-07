from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.config.settings import get_settings
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str) -> str: return pwd_context.hash(password)
def verify_password(password: str, hashed: str) -> bool: return pwd_context.verify(password, hashed)
def create_token(subject: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    return jwt.encode({"sub": subject, "type": token_type, "iat": now, "exp": now + expires_delta}, get_settings().jwt_secret_key, algorithm=get_settings().jwt_algorithm)
def create_access_token(subject: str) -> str: return create_token(subject, "access", timedelta(minutes=get_settings().access_token_expire_minutes))
def create_refresh_token(subject: str) -> str: return create_token(subject, "refresh", timedelta(days=get_settings().refresh_token_expire_days))
