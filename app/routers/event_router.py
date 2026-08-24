# Sự kiện/member endpoints
from fastapi import APIRouter, Request, Depends
import app.services.event_service as event_service
from app.schemas.event_schema import EventCreate, EventResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.api_schema import success_response
from app.dependencies.dependencies import get_current_user
from app.schemas.event_schema import EventUpdate


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
    event_response = EventResponse.model_validate(event_data)
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

    event_list = [EventResponse.model_validate(e).model_dump() for e in events]

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

    event_data = EventResponse.model_validate(event).model_dump()

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

    event_data = EventResponse.model_validate(updated_event).model_dump()

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