from sqlalchemy.orm import Session
from app.models.event_model import EventModel
from fastapi import Depends, HTTPException, status
from app.models.event_staff import EventStaffModel
from app.models.user_model import UserModel


def get_event_members(
    db: Session,
    event_id: int,
    current_user
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Không tìm thấy sự kiện")

    member_data = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id
    ).first()

    if not member_data:
        raise HTTPException(
            status_code=403, detail="Bạn không có quyền xem danh sách thành viên sự kiện này")

    members = (
        db.query(
            EventStaffModel.user_id,
            UserModel.full_name.label("user_name"),
            UserModel.email,
            EventStaffModel.role
        )
        .join(UserModel, EventStaffModel.user_id == UserModel.id)
        .filter(EventStaffModel.event_id == event_id)
        .all()
    )

    return members
