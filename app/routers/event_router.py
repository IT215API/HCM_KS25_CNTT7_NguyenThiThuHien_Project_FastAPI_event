# Sự kiện/member endpoints
from fastapi import APIRouter, Request, Depends
import app.services.event_service as event_service
from app.schemas.event_schema import EventCreate, EventResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.api_schema import success_response
from app.dependencies.dependencies import get_current_user
from app.schemas.event_schema import EventUpdate
from app.schemas.event_staff_schema import EventMemberResponse
from app.models.user_model import UserModel
from app.schemas.event_staff_schema import AddMemberSchema
from app.schemas.event_task_schema import EventTaskCreate, EventTaskResponse


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post("", status_code=201)
def create_event(
    request: Request, 
    event: EventCreate, 
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event_data = event_service.create_event(event, db, current_user)
    event_response = EventResponse.model_validate(
        event_data).model_dump(mode="json")
    return success_response(
        data=event_response,
        message="Tạo sự kiện thành công",
        request=request
    )


@router.get("", status_code=200)
def get_user_events(
    request: Request,
    search: str | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    events = event_service.get_user_events(db, current_user, search)

    event_list = [EventResponse.model_validate(e).model_dump(mode="json") for e in events]

    return success_response(
        request=request,
        data=event_list,
        message="Lấy danh sách sự kiện thành công"
    )


@router.get("/{event_id}", status_code=200)
def get_event_by_id(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    event = event_service.get_event_by_id(db, event_id, current_user)

    event_data = EventResponse.model_validate(event).model_dump(mode="json")

    return success_response(
        request=request,
        data=event_data,
        message="Lấy thông tin chi tiết sự kiện thành công"
    )


@router.patch("/{event_id}", status_code=200)
def update_event_owner(
    event_id: int,
    event_in: EventUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_event = event_service.update_event_owner(
        db=db,
        event_id=event_id,
        event_in=event_in,
        current_user=current_user
    )

    event_data = EventResponse.model_validate(updated_event).model_dump(mode="json")

    return success_response(
        request=request,
        data=event_data,
        message="Cập nhật sự kiện thành công"
    )


@router.delete("/{event_id}", status_code=200)
def delete_event_owner(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted_event_data = event_service.delete_event_owner(
        db=db,
        event_id=event_id,
        current_user=current_user
    )

    return success_response(
        request=request,
        data=deleted_event_data,
        message="Xóa sự kiện thành công"
    )



@router.post("/{event_id}/members", status_code=201)
def add_member(
    event_id: int,
    payload: AddMemberSchema,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    member_data = event_service.add_member_to_event(
        event_id=event_id,
        payload=payload,
        db=db,
        current_user=current_user
    )

    response_data = EventMemberResponse.model_validate(member_data).model_dump()

    return success_response(
        data=response_data,
        message="Thêm thành viên thành công",
        request=request
    )


@router.delete("/{event_id}/members/{user_id}", status_code=200)
def remove_member(
    event_id: int,
    user_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    event_service.remove_member_from_event(
        event_id=event_id,
        user_id=user_id,
        db=db,
        current_user=current_user
    )

    return success_response(
        data=None,
        message="Xóa thành viên khỏi sự kiện thành công",
        request=request
    )


@router.get("/{event_id}/members", status_code=200)
def get_event_members(
    event_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    members = event_service.get_event_members(
        db=db,
        event_id=event_id,
        current_user=current_user
    )

    members_data = [EventMemberResponse.model_validate(
        m).model_dump() for m in members]

    return success_response(
        request=request,
        data=members_data,
        message="Lấy danh sách thành viên thành công"
    )

# công việc sự kiện
@router.post("/{event_id}/event-tasks", status_code=201)
def create_task(
    event_id: int,
    event_task_in: EventTaskCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    task_data = event_service.create_event_task(
        event_id=event_id,
        event_task_in=event_task_in,
        db=db,
        current_user=current_user
    )

    task_response = EventTaskResponse.model_validate(task_data).model_dump(mode="json")

    return success_response(
        data=task_response,
        message="Tạo công việc sự kiện thành công",
        request=request
    )


@router.get("/{event_id}/event-tasks", status_code=200)
def get_tasks(
    event_id: int,
    request: Request,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    tasks = event_service.get_event_tasks(
        event_id=event_id,
        db=db,
        current_user=current_user,
        search=search,
        status=status,
        priority=priority,
        assignee_id=assignee_id,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        order=order
    )

    tasks_response = [EventTaskResponse.model_validate(task).model_dump(mode="json") for task in tasks]

    return success_response(
        data=tasks_response,
        message="Lấy danh sách công việc sự kiện thành công",
        request=request
    )
