# User endpoints
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserResponse
import app.services.user_service as user_service
from app.schemas.api_schema import success_response
from app.dependencies.dependencies import RoleChecker, get_current_user
from app.models.user_model import UserModel
from typing import Optional


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


@router.get("")
def get_all_users(
    request: Request,
    search: Optional[str] = Query(None, description="Tìm kiếm theo tên hoặc email"),
    is_active: Optional[bool] = Query(None, description="Lọc theo trạng thái hoạt động (true/false)"),
    db: Session = Depends(get_db),
    current_admin: UserModel = Depends(RoleChecker(["Admin"]))
):
    users = user_service.get_users(db, search=search, is_active=is_active)

    users_response = [UserResponse.model_validate(u) for u in users]

    return success_response(
        data=users_response,
        message="Lấy danh sách người dùng thành công",
        request=request
    )