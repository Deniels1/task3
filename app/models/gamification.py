"""Gamification models: badges."""

from sqlalchemy import String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class BadgeTemplate(Base, UUIDMixin, TimestampMixin):
    """Badge template defining achievement criteria."""
    __tablename__ = "badge_templates"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    icon_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    trigger_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )  # milestone, xp, streak, lesson

    trigger_conditions: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )  # JSON: {"count": 10} or {"threshold": 100}

    xp_reward: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    badges: Mapped[list["Badge"]] = relationship(
        "Badge",
        back_populates="template",
        lazy="selectin"
    )


class Badge(Base, UUIDMixin, TimestampMixin):
    """Badge earned by a child."""
    __tablename__ = "badges"

    child_id: Mapped[str] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    badge_template_id: Mapped[str] = mapped_column(
        ForeignKey("badge_templates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    earned_at: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationships
    child: Mapped["Child"] = relationship("Child", back_populates="badges")
    template: Mapped["BadgeTemplate"] = relationship("BadgeTemplate", back_populates="badges")
