from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from app.models.event_task_model import EventTaskModel
from app.models.user_model import UserModel
from app.models.event_staff_model import EventStaffModel


def get_event_task_detail(
    task_id: int,
    db: Session,
    current_user: UserModel
):
    task = db.query(EventTaskModel).filter(EventTaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Công việc không tồn tại")

    is_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == task.event_id,
        EventStaffModel.user_id == current_user.id
    ).first()

    if not is_member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền xem chi tiết công việc này"
        )

    return task
