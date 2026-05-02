"""Children endpoints."""

from fastapi import APIRouter, Query

from app.schemas.child import ChildCreate, ChildResponse, ChildProgress
from app.schemas.common import PaginatedResponse

router = APIRouter(prefix="/children", tags=["children"])


@router.get("", response_model=PaginatedResponse[ChildResponse])
async def get_children(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100)
):
    """Get all children for current parent with pagination."""
    items = [
        ChildResponse(
            id="child-1",
            name="Alice",
            age=6,
            xp_total=350,
            level_number=2,
            streak_current=5,
            streak_best=12,
            lessons_completed=8
        ),
        ChildResponse(
            id="child-2",
            name="Bob",
            age=7,
            xp_total=200,
            level_number=1,
            streak_current=3,
            streak_best=5,
            lessons_completed=4
        )
    ]
    return PaginatedResponse(
        items=items,
        total=2,
        page=page,
        page_size=page_size,
        total_pages=1
    )


@router.post("", response_model=ChildResponse)
async def create_child(data: ChildCreate):
    """Create new child profile."""
    return ChildResponse(
        id="new-child-id",
        name=data.name,
        age=data.age,
        xp_total=0,
        level_number=1,
        streak_current=0,
        streak_best=0,
        lessons_completed=0
    )


@router.get("/{child_id}", response_model=ChildResponse)
async def get_child(child_id: str):
    """Get child by ID."""
    return ChildResponse(
        id=child_id,
        name="Alice",
        age=6,
        xp_total=350,
        level_number=2,
        streak_current=5,
        streak_best=12,
        lessons_completed=8
    )


@router.get("/{child_id}/progress", response_model=ChildProgress)
async def get_child_progress(child_id: str):
    """Get child progress."""
    return ChildProgress(
        child_id=child_id,
        name="Alice",
        xp_total=350,
        level_number=2,
        streak_current=5,
        lessons_completed=8,
        accuracy_rate=85.5
    )
