"""Admin schemas."""

from pydantic import BaseModel
from datetime import datetime


class ActivityLogResponse(BaseModel):
    id: str
    admin_id: str | None
    action: str
    resource_type: str
    resource_id: str
    before_snapshot: str | None
    after_snapshot: str | None
    created_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_parents: int
    total_children: int
    total_lessons_completed: int
    total_exercises_completed: int
    average_accuracy: float
    active_streaks: int
