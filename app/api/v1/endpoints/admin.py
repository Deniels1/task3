"""Admin endpoints."""

from fastapi import APIRouter, HTTPException

from app.schemas.admin import ActivityLogResponse, StatsResponse
from app.schemas.curriculum import UnitResponse, LessonResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/logs", response_model=list[ActivityLogResponse])
async def get_activity_logs():
    """Get admin activity logs. Admin only."""
    return [
        ActivityLogResponse(
            id="log-1",
            admin_id="admin-1",
            action="create",
            resource_type="lesson",
            resource_id="lesson-1",
            before_snapshot=None,
            after_snapshot='{"title": "Letter A"}',
            created_at="2024-01-15T10:00:00"
        ),
        ActivityLogResponse(
            id="log-2",
            admin_id="admin-1",
            action="publish",
            resource_type="unit",
            resource_id="unit-1",
            before_snapshot='{"published": false}',
            after_snapshot='{"published": true}',
            created_at="2024-01-16T14:00:00"
        )
    ]


@router.get("/stats", response_model=StatsResponse)
async def get_platform_stats():
    """Get platform-wide statistics. Admin only."""
    return StatsResponse(
        total_parents=150,
        total_children=230,
        total_lessons_completed=1200,
        total_exercises_completed=8500,
        average_accuracy=78.5,
        active_streaks=45
    )


@router.post("/units", response_model=UnitResponse)
async def create_unit(data: dict):
    """Create new unit. Admin only."""
    return UnitResponse(
        id="new-unit-id",
        title=data.get("title", "New Unit"),
        description=data.get("description"),
        order_index=1,
        published=False
    )


@router.post("/lessons", response_model=LessonResponse)
async def create_lesson(data: dict):
    """Create new lesson. Admin only."""
    return LessonResponse(
        id="new-lesson-id",
        unit_id=data.get("unit_id", "unit-1"),
        title=data.get("title", "New Lesson"),
        exercise_type=data.get("exercise_type", "phonics"),
        difficulty=data.get("difficulty", 1),
        order_index=1,
        published=False
    )
