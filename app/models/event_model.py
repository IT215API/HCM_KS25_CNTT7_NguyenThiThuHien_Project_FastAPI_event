# Model event/eventStaff
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # 1 user - N event owner
    user = relationship("UserModel", back_populates="owner_events")

    # 1 event - N event task
    event_tasks = relationship("EventTaskModel", back_populates="event")

    # 1 event - N event staff
    event_staffs = relationship("EventStaffModel", back_populates="event")
