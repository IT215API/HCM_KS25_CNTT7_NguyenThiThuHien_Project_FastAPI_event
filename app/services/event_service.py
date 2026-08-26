from fastapi import Depends, HTTPException, status
from app.schemas.event_schema import EventCreate
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.dependencies.dependencies import get_current_user
from app.models.event_model import EventModel
from app.models.user_model import UserModel
from app.models.event_staff_model import EventStaffModel, Role
from app.schemas.event_schema import EventUpdate, EventResponse
from app.schemas.event_staff_schema import AddMemberSchema
from app.schemas.event_task_schema import EventTaskCreate
from app.models.event_task_model import EventTaskModel


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

    staff_member = EventStaffModel(
        event_id=new_event.id,
        user_id=current_user.id,
        role=Role.OWNER
    )
    db.add(staff_member)
    db.commit()

    return new_event


def get_user_events(
    db: Session, 
    current_user, search: str | None = None
):
    query_user = (
        db.query(EventModel)
        .join(EventStaffModel, EventModel.id == EventStaffModel.event_id)
        .filter(EventStaffModel.user_id == current_user.id)
    )

    if search is not None:
        search_clean = search.strip()
        if search_clean:
            query_user = query_user.filter(EventModel.name.ilike(f"%{search_clean}%"))

    return query_user.all()


def get_event_by_id(
    db: Session, 
    event_id: int, 
    current_user
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy sự kiện"
        )

    member = (
        db.query(EventStaffModel)
        .filter(EventStaffModel.event_id == event_id, EventStaffModel.user_id == current_user.id)
        .first()
    )

    if not member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền truy cập sự kiện này"
        )

    return event


def update_event_owner(
    db: Session,
    event_id: int, 
    event_in: EventUpdate, 
    current_user
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Không tìm thấy sự kiện")

    if event.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Chỉ có Owner mới có quyền cập nhật")

    if event_in.name is not None:
        clean_name = event_in.name.strip()
        if not clean_name:
            raise HTTPException(
                status_code=400, detail="Tên sự kiện không được để trống")
        event.name = clean_name

    if event_in.description:
        event.description = event_in.description.strip()

    db.commit()
    db.refresh(event)
    return event


def delete_event_owner(
    db: Session,
    event_id: int,
    current_user
):
    event = db.query(EventModel).filter(EventModel.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Không tìm thấy sự kiện")

    if event.owner_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Chỉ có Owner mới có quyền xóa")

    event_data = EventResponse.model_validate(event).model_dump()

    db.delete(event)
    db.commit()

    return event_data


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
        raise HTTPException(
            status_code=403, detail="Chỉ OWNER mới có quyền xóa thành viên")

    if user_id == current_user.id:
        raise HTTPException(
            status_code=400,
            detail="Bạn không thể tự xóa chính mình khỏi sự kiện"
        )

    target_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == user_id
    ).first()
    if not target_member:
        raise HTTPException(
            status_code=404, detail="Thành viên không tồn tại trong sự kiện này")

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

# công việc sự kiện
def create_event_task(
    event_id: int,
    event_task_in: EventTaskCreate,
    db: Session,
    current_user: UserModel
):
    is_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id
    ).first()

    if not is_member:
        event_exists = db.query(EventModel.id).filter(
            EventModel.id == event_id).first()
        if not event_exists:
            raise HTTPException(
                status_code=404, detail="Sự kiện không tồn tại")
        raise HTTPException(
            status_code=403, detail="Bạn không phải thành viên của sự kiện này")

    if event_task_in.assignee_id is not None and event_task_in.assignee_id <= 0:
        event_task_in.assignee_id = current_user.id

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
    current_user: UserModel,
    search: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
    order: str = "desc"
):
    if assignee_id is not None and assignee_id <= 0:
        assignee_id = None
    if limit <= 0:
        limit = 10
    if offset < 0:
        offset = 0

    is_member = db.query(EventStaffModel).filter(
        EventStaffModel.event_id == event_id,
        EventStaffModel.user_id == current_user.id
    ).first()

    if not is_member:
        event_exists = db.query(EventModel.id).filter(EventModel.id == event_id).first()
        if not event_exists:
            raise HTTPException(
                status_code=404, detail="Sự kiện không tồn tại")
        raise HTTPException(
            status_code=403,
            detail="Bạn không có quyền xem danh sách công việc của sự kiện này"
        )

    query = db.query(EventTaskModel).filter(EventTaskModel.event_id == event_id)

    if search is not None:
        search_clean = search.strip()
        if search_clean:
            query = query.filter(EventTaskModel.title.ilike(f"%{search_clean}%"))

    if status is not None:
        query = query.filter(EventTaskModel.status == status)

    if priority is not None:
        query = query.filter(EventTaskModel.priority == priority)

    if assignee_id is not None:
        query = query.filter(EventTaskModel.assignee_id == assignee_id)

    if sort_by == "due_date":
        if order.lower() == "asc":
            query = query.order_by(EventTaskModel.due_date.asc())
        else:
            query = query.order_by(EventTaskModel.due_date.desc())
    else:
        if order.lower() == "asc":
            query = query.order_by(EventTaskModel.created_at.asc())
        else:
            query = query.order_by(EventTaskModel.created_at.desc())

    query = query.offset(offset).limit(limit)

    return query.all()
