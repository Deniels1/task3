"""Leaderboard endpoints."""

from fastapi import APIRouter

from app.schemas.progress import LeaderboardEntry

router = APIRouter(prefix="/leaderboard", tags=["gamification"])


@router.get("", response_model=list[LeaderboardEntry])
async def get_leaderboard():
    """Get global leaderboard."""
    return [
        LeaderboardEntry(
            child_id="child-1",
            name="Alice",
            xp_total=350,
            level_number=2,
            streak_current=5,
            rank=1
        ),
        LeaderboardEntry(
            child_id="child-2",
            name="Bob",
            xp_total=200,
            level_number=1,
            streak_current=3,
            rank=2
        )
    ]
