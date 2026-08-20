# Model eventTask
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class EventTaskModel(Base):
    __tablename__ = "event_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(255), nullable=False)
    priority = Column(String(255), nullable=False)
    due_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = Column(DateTime, default=lambda: datetime.now(
        timezone.utc), nullable=False)

    # 1 event - N event tasks
    event = relationship("EventModel", back_populates="event_tasks")

    # 1 user - N event tasks
    user = relationship("UserModel", back_populates="event_tasks")
