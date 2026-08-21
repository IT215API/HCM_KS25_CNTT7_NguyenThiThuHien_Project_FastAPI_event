# Model user
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from sqlalchemy.orm import relationship


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(255), default="User")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # 1 user - N event owner
    owner_events = relationship("EventModel", back_populates="user")

    # 1 user - N event staff
    event_staffs = relationship("EventStaffModel", back_populates="user")

    # 1 user - N event task (assignee)
    event_tasks = relationship("EventTaskModel", back_populates="user")
