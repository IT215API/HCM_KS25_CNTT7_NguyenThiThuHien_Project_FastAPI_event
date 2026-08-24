from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.event_schema import EventCreate
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.dependencies.dependencies import get_current_user
from app.models.event_model import EventModel
from app.schemas.api_schema import success_response
from app.models.user_model import UserModel


def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    user = db.query(UserModel).filter(UserModel.id == current_user.id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại"
        )

    clean_name_event = event.name.strip()
    if not clean_name_event:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên sự kiện không được để trống"
        )

    if len(clean_name_event) > 255:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên sự kiện không được vượt quá 255 ký tự"
        )
    
    new_event = EventModel(
        name=event.name,
        description=event.description,
        owner_id=current_user.id
    )

    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return new_event
