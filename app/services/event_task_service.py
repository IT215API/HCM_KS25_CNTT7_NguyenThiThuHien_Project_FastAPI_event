from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.event_task_model import EventTaskModel
from app.models.user_model import UserModel
from app.models.event_staff_model import EventStaffModel, Role
from app.schemas.event_task_schema import EventTaskUpdate



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


def update_event_task(
    task_id: int,
    event_task_in: EventTaskUpdate,
    db: Session,
    current_user: UserModel
):
    task = db.query(EventTaskModel).filter(EventTaskModel.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Công việc không tồn tại")

    staff_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == task.event_id,
        EventStaffModel.user_id == current_user.id
    ).first()

    if not staff_member:
        raise HTTPException(status_code=403, detail="Bạn không thuộc sự kiện này")

    is_owner = (staff_member.role == Role.OWNER)
    is_assignee = (task.assignee_id == current_user.id)

    if not (is_owner or is_assignee):
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền cập nhật công việc này"
        )

    if is_assignee and not is_owner:
        if event_task_in.assignee_id is not None and event_task_in.assignee_id != task.assignee_id:
            raise HTTPException(
                status_code=403,
                detail="Chỉ Trưởng ban tổ chức (Owner) mới có quyền đổi người phụ trách"
            )
    
    if is_owner and event_task_in.assignee_id is not None:
        if event_task_in.assignee_id > 0:
            is_assignee_member = db.query(EventStaffModel).filter(
                EventStaffModel.event_id == task.event_id,
                EventStaffModel.user_id == event_task_in.assignee_id
            ).first()
            if not is_assignee_member:
                raise HTTPException(
                    status_code=400,
                    detail="Người được giao việc phải là thành viên trong sự kiện"
                )
            task.assignee_id = event_task_in.assignee_id
        else:
            task.assignee_id = None

    if event_task_in.title is not None:
        task.title = event_task_in.title

    if event_task_in.description is not None:
        task.description = event_task_in.description

    if event_task_in.status is not None:
        task.status = event_task_in.status

    if event_task_in.priority is not None:
        task.priority = event_task_in.priority

    if event_task_in.due_date is not None:
        task.due_date = event_task_in.due_date

    db.add(task)
    db.commit()
    db.refresh(task)

    return task
