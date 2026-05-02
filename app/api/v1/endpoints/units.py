"""Units endpoints."""

from fastapi import APIRouter, Query

from app.schemas.curriculum import UnitResponse, LessonResponse
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/units", tags=["curriculum"])


@router.get("", response_model=PaginatedResponse[UnitResponse])
async def get_units(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get all published units with pagination."""
    items = [
        UnitResponse(
            id="unit-1",
            title="Phonics Level 1",
            description="Learn basic letter sounds",
            order_index=1,
            published=True
        ),
        UnitResponse(
            id="unit-2",
            title="Sight Words",
            description="Common words recognition",
            order_index=2,
            published=True
        )
    ]
    return PaginatedResponse(
        items=items,
        total=2,
        page=page,
        page_size=page_size,
        total_pages=1
    )


@router.get("/{unit_id}/lessons", response_model=list[LessonResponse])
async def get_unit_lessons(unit_id: str):
    """Get lessons for a unit."""
    return [
        LessonResponse(
            id="lesson-1",
            unit_id=unit_id,
            title="Letter A",
            exercise_type="phonics",
            difficulty=1,
            order_index=1,
            published=True
        ),
        LessonResponse(
            id="lesson-2",
            unit_id=unit_id,
            title="Letter B",
            exercise_type="phonics",
            difficulty=1,
            order_index=2,
            published=True
        )
    ]
