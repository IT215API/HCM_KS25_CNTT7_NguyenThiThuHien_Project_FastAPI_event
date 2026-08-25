from sqlalchemy.orm import Session
from app.models.event_model import EventModel
from fastapi import Depends, HTTPException, status
from app.models.event_staff import EventStaffModel
from app.models.user_model import UserModel
from app.schemas.event_staff_schema import AddMemberSchema


def add_member_to_event(
    event_id: int,
    payload: AddMemberSchema,
    db: Session,
    current_user: UserModel
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Sự kiện không tồn tại")

    is_owner = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id,
        EventStaffModel.role == "OWNER"
    ).first()
    if not is_owner:
        raise HTTPException(
            status_code=403, detail="Chỉ OWNER mới có quyền thêm thành viên")

    target_user = db.query(UserModel).filter(
        UserModel.id == payload.user_id).first()
    if not target_user:
        raise HTTPException(
            status_code=404, detail="Người dùng cần thêm không tồn tại")

    existing_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == payload.user_id
    ).first()
    if existing_member:
        raise HTTPException(
            status_code=400, detail="Thành viên này đã có trong sự kiện")

    new_member = EventStaffModel(
        event_id=event_id,
        user_id=payload.user_id,
        role=payload.role or "MEMBER"
    )
    db.add(new_member)
    db.commit()

    return {
        "user_id": target_user.id,
        "user_name": getattr(target_user, "name", target_user.username if hasattr(target_user, "username") else ""),
        "email": target_user.email,
        "role": new_member.role
    }


def remove_member_from_event(
    event_id: int, 
    user_id: int, 
    db: Session, 
    current_user: UserModel
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Sự kiện không tồn tại")

    is_owner = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id,
        EventStaffModel.role == "OWNER"
    ).first()
    if not is_owner:
        raise HTTPException(status_code=403, detail="Chỉ OWNER mới có quyền xóa thành viên")

    target_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == user_id
    ).first()
    if not target_member:
        raise HTTPException(status_code=404, detail="Thành viên không tồn tại trong sự kiện này")

    if target_member.role == "OWNER":
        owner_count = db.query(EventStaffModel).filter(
            EventStaffModel.event_id == event_id,
            EventStaffModel.role == "OWNER"
        ).count()
        
        if owner_count <= 1:
            raise HTTPException(
                status_code=400, 
                detail="Không thể xóa OWNER cuối cùng của sự kiện"
            )

    db.delete(target_member)
    db.commit()

    return True


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



