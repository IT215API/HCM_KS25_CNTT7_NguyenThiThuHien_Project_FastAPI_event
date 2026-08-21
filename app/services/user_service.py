from app.core.security import verify_password, create_access_token
from sqlalchemy.orm import Session
import app.schemas.user_schema as user_schema
from app.models.user_model import UserModel
from fastapi import HTTPException, status
from app.core.security import hash_password
from typing import Optional
from sqlalchemy import or_


def create_user(db: Session, user: user_schema.UserCreate):
    user_data = db.query(UserModel).filter(UserModel.email == user.email).first()

    if user_data:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    hashed_password = hash_password(user.password)

    new_user = UserModel(
        email=user.email, 
        password_hash=hashed_password, 
        full_name=user.full_name
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def authenticate_user(db: Session, user: user_schema.UserLogin) -> dict:
    user_data = db.query(UserModel).filter(UserModel.email == user.email).first()

    if not user_data or not verify_password(user.password, user_data.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user_data.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã bị tạm khóa"
        )

    access_token = create_access_token(data={"sub": user_data.email, "role": user_data.role})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


def get_users(
    db: Session,
    search: Optional[str] = None,
    is_active: Optional[bool] = None
) -> list[UserModel]:
    query = db.query(UserModel)

    if search:
        search_filter = f"%{search.strip()}%"
        query = query.filter(or_(
                UserModel.full_name.ilike(search_filter),
                UserModel.email.ilike(search_filter)
            )
        )

    if is_active is not None:
        query = query.filter(UserModel.is_active == is_active)

    return query.order_by(UserModel.created_at.desc()).all()
