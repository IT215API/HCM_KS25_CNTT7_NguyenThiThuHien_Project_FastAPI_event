# Sự kiện/member endpoints
from fastapi import APIRouter, Request, Depends
import app.services.event_service as event_service
from app.schemas.event_schema import EventCreate, EventResponse
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.api_schema import success_response
from app.dependencies.dependencies import get_current_user


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
