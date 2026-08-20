# Model event/eventStaff
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

event_staff = Table(
    "event_staff",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("role", String(255), nullable=False),
    Column("joined_at", DateTime,  default=lambda: datetime.now(timezone.utc))
)

class EventModel(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # 1 user - N event (owner)
    owner = relationship("EventModel", back_populates="owner_events", foreign_keys=[owner_id])

    # N user - N event
    staffs = relationship("UserModel", secondary="event_staff", back_populates="events")

    # 1 event - N event tasks
    event_tasks = relationship("EventTaskModel", back_populates="event")

