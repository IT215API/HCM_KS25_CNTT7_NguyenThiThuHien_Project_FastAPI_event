# User endpoints
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse, UserLogin
import app.services.user_service as user_service
from app.schemas.api_schema import success_response
from app.dependencies.dependencies import RoleChecker, get_current_user
from app.models.user_model import UserModel


router = APIRouter(
    prefix="/api/users",
    tags=["User"]
)


@router.get("/me")
def get_current_user_profile(
    request: Request,
    current_user: UserModel = Depends(get_current_user)
):
    user_data = UserResponse.model_validate(current_user)

    return success_response(
        data=user_data,
        message="Lấy thông tin tài khoản thành công",
        request=request
    )
