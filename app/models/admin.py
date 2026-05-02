"""Admin activity log model."""

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class ActivityLog(Base, UUIDMixin, TimestampMixin):
    """Log of admin actions."""
    __tablename__ = "activity_logs"

    admin_id: Mapped[str] = mapped_column(
        ForeignKey("parents.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    action: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    # create, update, delete, publish

    resource_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )  # unit, lesson, exercise

    resource_id: Mapped[str] = mapped_column(String(36), nullable=False)

    before_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    after_snapshot: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    admin: Mapped["Parent"] = relationship("Parent", back_populates="activity_logs")
