from sqlalchemy.orm import Session
import app.schemas.user_schema as user_schema
from app.models.user_model import UserModel
from fastapi import HTTPException
from app.core.security import hash_password


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
