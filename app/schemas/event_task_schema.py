from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.models.event_task_model import Status, Priority


class EventTaskBase(BaseModel):
    title: str = Field(..., max_length=255)
    description: str | None = None
    status: Status = Field(default=Status.TODO)
    priority: Priority = Field(default=Priority.MEDIUM)
    due_date: datetime | None = None


class EventTaskCreate(EventTaskBase):
    assignee_id: Optional[int] = None


class EventTaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    assignee_id: int | None = None
    status: Status | None = None
    priority: Priority | None = None
    due_date: datetime | None = None


class EventTaskResponse(EventTaskBase):
    id: int
    event_id: int
    assignee_id: int | None = None
    created_at: datetime

    class Config():
        from_attributes=True