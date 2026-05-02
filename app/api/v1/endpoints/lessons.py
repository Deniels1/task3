"""Lessons endpoints."""

from fastapi import APIRouter

from app.schemas.curriculum import LessonResponse, ExerciseResponse
from app.schemas.progress import LessonCompleteRequest, LessonCompleteResponse

router = APIRouter(prefix="/lessons", tags=["curriculum"])


@router.get("/{lesson_id}", response_model=LessonResponse)
async def get_lesson(lesson_id: str):
    """Get lesson by ID."""
    return LessonResponse(
        id=lesson_id,
        unit_id="unit-1",
        title="Letter A",
        exercise_type="phonics",
        difficulty=1,
        order_index=1,
        published=True
    )


@router.get("/{lesson_id}/exercises", response_model=list[ExerciseResponse])
async def get_lesson_exercises(lesson_id: str):
    """Get exercises for a lesson."""
    return [
        ExerciseResponse(
            id="ex-1",
            lesson_id=lesson_id,
            type="match",
            content='{"question": "Match A to /a/"}',
            difficulty=1,
            order_index=1
        ),
        ExerciseResponse(
            id="ex-2",
            lesson_id=lesson_id,
            type="tracing",
            content='{"letter": "A"}',
            difficulty=1,
            order_index=2
        )
    ]


@router.post("/{lesson_id}/complete", response_model=LessonCompleteResponse)
async def complete_lesson(lesson_id: str, data: LessonCompleteRequest):
    """Complete a lesson and update XP, streak, level."""
    # Simulate gamification logic
    xp_earned = 100 + (1 - 1) * 20  # difficulty 1
    return LessonCompleteResponse(
        xp_earned=xp_earned,
        total_xp=350 + xp_earned,
        new_level=2,
        level_up=False,
        new_streak=6,
        streak_updated=True,
        badges_earned=["first_lesson"]
    )
