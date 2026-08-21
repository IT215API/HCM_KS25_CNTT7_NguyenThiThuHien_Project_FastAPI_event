# hash password, JWT encode/decode
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import settings

def hash_password(password: str, cost_factor: int = 12) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=cost_factor)
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    return hashed_bytes.decode('utf-8')