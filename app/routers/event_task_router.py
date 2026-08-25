# Công việc sự kiện endpoints
from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.user_model import UserModel
from app.dependencies.dependencies import get_current_user
import app.services.event_task_service as event_task_service
from app.schemas.event_task_schema import EventTaskResponse
from app.schemas.api_schema import success_response


router = APIRouter(
    prefix="/event-tasks",
    tags=["Event Tasks"]
)


@router.get("/event-tasks/{task_id}", status_code=200)
def get_task_detail(
    task_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task_data = event_task_service.get_event_task_detail(
        task_id=task_id,
        db=db,
        current_user=current_user
    )

    task_response = EventTaskResponse.model_validate(
        task_data).model_dump(mode="json")

    return success_response(
        data=task_response,
        message="Lấy thông tin chi tiết công việc thành công",
        request=request
    )
