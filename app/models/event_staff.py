from app.db.database import Base
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import enum

class Role(str, enum.Enum):
    OWNER = "owner"
    MEMBER = "member"

class EventStaffModel(Base):
    __tablename__ = "event_staffs"

    event_id = Column(Integer, ForeignKey("events.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(SQLEnum(Role), default=Role.MEMBER, nullable=False)
    joined_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # 1 user - N event staff
    user = relationship("UserModel", back_populates="event_staffs")

    # 1 event - N event staff
    event = relationship("EventModel", back_populates="event_staffs")
