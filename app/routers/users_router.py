# User endpoints
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserResponse
import app.services.user_service as user_service
from app.schemas.api_schema import success_response
from app.dependencies.dependencies import RoleChecker
from app.models.user_model import UserModel


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


@router.get("/users")
def get_all_users_for_admin(
    request: Request,
    current_user: UserModel = Depends(RoleChecker(["Admin", "Manager"]))
):
    return success_response(
        data={"message": f"Welcome Admin {current_user.full_name}"},
        message="Truy cập danh sách người dùng thành công",
        request=request
    )
