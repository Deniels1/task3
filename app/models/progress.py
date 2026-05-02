"""Progress tracking models."""

from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, UUIDMixin, TimestampMixin


class LessonProgress(Base, UUIDMixin, TimestampMixin):
    """Records child's progress on a lesson."""
    __tablename__ = "lesson_progress"

    child_id: Mapped[str] = mapped_column(
        ForeignKey("children.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    lesson_id: Mapped[str] = mapped_column(
        ForeignKey("lessons.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="in_progress",
        nullable=False
    )  # in_progress, completed

    xp_earned: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    child: Mapped["Child"] = relationship("Child", back_populates="lesson_progresses")
    lesson: Mapped["Lesson"] = relationship("Lesson", back_populates="progress_records")
    exercise_results: Mapped[list["ExerciseResult"]] = relationship(
        "ExerciseResult",
        back_populates="lesson_progress",
        lazy="selectin",
        cascade="all, delete-orphan"
    )


class ExerciseResult(Base, UUIDMixin, TimestampMixin):
    """Records child's result on a single exercise."""
    __tablename__ = "exercise_results"

    progress_id: Mapped[str] = mapped_column(
        ForeignKey("lesson_progress.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    exercise_id: Mapped[str] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    time_spent_seconds: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    answer_data: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    lesson_progress: Mapped["LessonProgress"] = relationship(
        "LessonProgress",
        back_populates="exercise_results"
    )
    exercise: Mapped["Exercise"] = relationship("Exercise", back_populates="results")
