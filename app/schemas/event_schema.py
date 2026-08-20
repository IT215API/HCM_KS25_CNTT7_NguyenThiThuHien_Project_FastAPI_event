from pydantic import BaseModel
from datetime import datetime


class EventBase(BaseModel):
    name: str
    description: str | None = None


class EventCreate(EventBase):
    owner_id: int


class EventUpdate(EventBase):
    name: str | None = None
    description: str | None = None


class EventResponse(BaseModel):
    id: int
    owner_id: int
    created_at: datetime

    class Config():
        from_attributes=True