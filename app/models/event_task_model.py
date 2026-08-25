# Model eventTask
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from datetime import datetime, timezone
from sqlalchemy.orm import relationship
import enum


class Status(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class Priority(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class EventTaskModel(Base):
    __tablename__ = "event_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(SQLEnum(Status), nullable=False)
    priority = Column(SQLEnum(Priority), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # 1 event - N event task
    event = relationship("EventModel", back_populates="event_tasks")

    # 1 user - N event task (assignee)
    user = relationship("UserModel", back_populates="event_tasks")
