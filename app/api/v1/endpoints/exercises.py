"""Exercises endpoints."""

from fastapi import APIRouter

from app.schemas.curriculum import ExerciseResponse
from app.schemas.progress import LessonCompleteResponse

router = APIRouter(prefix="/exercises", tags=["curriculum"])


@router.get("/{exercise_id}", response_model=ExerciseResponse)
async def get_exercise(exercise_id: str):
    """Get exercise by ID."""
    return ExerciseResponse(
        id=exercise_id,
        lesson_id="lesson-1",
        type="match",
        content='{"question": "Match A to /a/"}',
        difficulty=1,
        order_index=1
    )


@router.post("/{exercise_id}/submit", response_model=dict)
async def submit_exercise(exercise_id: str, answer: dict):
    """Submit exercise answer."""
    correct = answer.get("answer") == "A"
    return {
        "exercise_id": exercise_id,
        "correct": correct,
        "xp_earned": 10 if correct else 0,
        "feedback": "Correct!" if correct else "Try again!"
    }
