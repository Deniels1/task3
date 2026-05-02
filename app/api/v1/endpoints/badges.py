"""Badges endpoints."""

from fastapi import APIRouter

from app.schemas.badge import BadgeResponse, BadgeTemplateResponse

router = APIRouter(prefix="/badges", tags=["gamification"])


@router.get("/templates", response_model=list[BadgeTemplateResponse])
async def get_badge_templates():
    """Get all badge templates."""
    return [
        BadgeTemplateResponse(
            id="bt-1",
            name="First Lesson",
            description="Complete your first lesson",
            icon_url=None,
            trigger_type="milestone",
            xp_reward=50
        ),
        BadgeTemplateResponse(
            id="bt-2",
            name="XP 100",
            description="Earn 100 XP",
            icon_url=None,
            trigger_type="xp",
            xp_reward=0
        ),
        BadgeTemplateResponse(
            id="bt-3",
            name="Streak 7",
            description="7 days streak",
            icon_url=None,
            trigger_type="streak",
            xp_reward=100
        )
    ]


@router.get("/children/{child_id}", response_model=list[BadgeResponse])
async def get_child_badges(child_id: str):
    """Get badges earned by a child."""
    return [
        BadgeResponse(
            id="badge-1",
            child_id=child_id,
            badge_template_id="bt-1",
            template_name="First Lesson",
            description="Complete your first lesson",
            earned_at="2024-01-15"
        )
    ]
