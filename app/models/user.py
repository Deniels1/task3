"""User models: Parent and Child."""
 
from datetime import datetime
from typing import List
 
from sqlalchemy import String, Boolean, Integer, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
 
from app.db.base import Base, UUIDMixin, TimestampMixin
 
 
class Parent(Base, UUIDMixin, TimestampMixin):
    """Parent/Guardian user account."""
    __tablename__ = "parents"
    
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
 
    # Relationships
    children: Mapped[List["Child"]] = relationship(
        "Child",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    notifications: Mapped[List["Notification"]] = relationship(
        "Notification",
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    activity_logs: Mapped[List["ActivityLog"]] = relationship(
        "ActivityLog",
        back_populates="admin",
        lazy="selectin"
    )
 
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
 
 
class Child(Base, UUIDMixin, TimestampMixin):
    """Child learner profile."""
    __tablename__ = "children"
    
    parent_id: Mapped[str] = mapped_column(
        ForeignKey("parents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    
    # Gamification stats
    xp_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)
    level_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    streak_current: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_best: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    streak_last_activity_date: Mapped[str | None] = mapped_column(String(10), nullable=True)
    
    # Statistics
    lessons_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    accuracy_rate: Mapped[float] = mapped_column(Integer, default=0, nullable=False)
    
    # Tracking
    last_activity_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, index=True)
    
    # Relationships
    parent: Mapped["Parent"] = relationship(
        "Parent",
        back_populates="children",
        lazy="joined"
    )
    lesson_progresses: Mapped[List["LessonProgress"]] = relationship(
        "LessonProgress",
        back_populates="child",
        cascade="all, delete-orphan",
        lazy="selectin"
    )
    badges: Mapped[List["Badge"]] = relationship(
        "Badge",
        back_populates="child",
        cascade="all, delete-orphan",
        lazy="selectin"
    )