from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserBase(BaseModel):
   email: EmailStr
   full_name: str


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes=True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
