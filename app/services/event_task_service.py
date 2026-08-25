from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.event_model import EventModel
from app.models.event_staff_model import EventStaffModel
from app.models.event_task_model import EventTaskModel
from app.models.user_model import UserModel
from app.schemas.event_task_schema import EventTaskCreate


def create_event_task(
    event_id: int,
    event_task_in: EventTaskCreate,
    db: Session,
    current_user: UserModel
):
    if event_task_in.assignee_id is not None and event_task_in.assignee_id <= 0:
        event_task_in.assignee_id = None

    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Sự kiện không tồn tại")

    is_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id
    ).first()
    if not is_member:
        raise HTTPException(
            status_code=403, detail="Bạn không phải thành viên của sự kiện này")

    if event_task_in.assignee_id:
        is_assignee_member = db.query(EventStaffModel).filter(
            EventStaffModel.event_id == event_id,
            EventStaffModel.user_id == event_task_in.assignee_id
        ).first()
        if not is_assignee_member:
            raise HTTPException(
                status_code=400,
                detail="Người được giao việc phải là thành viên trong sự kiện"
            )

    new_task = EventTaskModel(
        event_id=event_id,
        title=event_task_in.title,
        description=event_task_in.description,
        assignee_id=event_task_in.assignee_id,
        status=event_task_in.status,
        priority=event_task_in.priority,
        due_date=event_task_in.due_date
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


def get_event_tasks(
    event_id: int,
    db: Session,
    current_user: UserModel
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Sự kiện không tồn tại")

    is_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id
    ).first()
    if not is_member:
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền xem danh sách công việc của sự kiện này"
        )

    tasks = db.query(EventTaskModel).filter(
        EventTaskModel.event_id == event_id
    ).all()

    return tasks
