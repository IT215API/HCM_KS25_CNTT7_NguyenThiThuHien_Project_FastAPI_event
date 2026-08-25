# Công việc sự kiện endpoints
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.dependencies.dependencies import get_current_user
from app.models.user_model import UserModel
from app.schemas.event_task_schema import EventTaskCreate, EventTaskResponse
from app.services import event_task_service
from app.schemas.api_schema import success_response


router = APIRouter(
    prefix="/event-tasks",
    tags=["Event Tasks"]
)


@router.post("/{event_id}/event-tasks", status_code=201)
def create_task(
    event_id: int,
    event_task_in: EventTaskCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task_data = event_task_service.create_event_task(
        event_id=event_id,
        event_task_in=event_task_in,
        db=db,
        current_user=current_user
    )

    task_response = EventTaskResponse.model_validate(task_data).model_dump()

    return success_response(
        data=task_response,
        message="Tạo công việc sự kiện thành công",
        request=request
    )


@router.get("/{event_id}/event-tasks", status_code=200)
def get_tasks(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    tasks = event_task_service.get_event_tasks(
        event_id=event_id,
        db=db,
        current_user=current_user
    )

    tasks_response = [EventTaskResponse.model_validate(task).model_dump() for task in tasks]

    return success_response(
        data=tasks_response,
        message="Lấy danh sách công việc sự kiện thành công",
        request=request
    )
