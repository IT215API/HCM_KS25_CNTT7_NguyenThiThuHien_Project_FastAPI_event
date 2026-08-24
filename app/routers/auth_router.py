# Register/Login
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
import app.services.user_service as user_service
from app.schemas.api_schema import success_response
from fastapi.security import OAuth2PasswordRequestForm
from app.dependencies.dependencies import get_current_user
from app.core.security import create_access_token


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=201)
def register_user(request: Request, user_data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user_data)
    user_response = UserResponse.model_validate(user)
    return success_response(
        data=user_response,
        message="Tạo tài khoản thành công",
        request=request
    )


@router.post("/login")
def login(
    user: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    token_data = user_service.authenticate_user(
        db, 
        email=user.username,
        password=user.password
    )

    return user_service.authenticate_user(
        db=db,
        email=user.username,
        password=user.password
    )


@router.post("/refresh")
def refresh_token(
    request: Request,
    current_user=Depends(get_current_user)
):
    new_access_token = create_access_token(
        data={"sub": current_user.email}
    )

    return success_response(
        data={"access_token": new_access_token, "token_type": "bearer"},
        message="Cấp lại access token thành công",
        request=request
    )
