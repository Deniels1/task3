"""Notification model."""

from sqlalchemy import String, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class Notification(Base, UUIDMixin, TimestampMixin):
    """Notification sent to parent."""
    __tablename__ = "notifications"

    parent_id: Mapped[str] = mapped_column(
        ForeignKey("parents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    notification_type: Mapped[str] = mapped_column(
        String(50),
        default="general",
        nullable=False
    )  # milestone, streak_reminder, weekly_summary

    is_read: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationships
    parent: Mapped["Parent"] = relationship("Parent", back_populates="notifications")
