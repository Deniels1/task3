"""Badge schemas."""

from pydantic import BaseModel
from datetime import datetime


class BadgeTemplateResponse(BaseModel):
    id: str
    name: str
    description: str
    icon_url: str | None
    trigger_type: str
    xp_reward: int

    class Config:
        from_attributes = True


class BadgeResponse(BaseModel):
    id: str
    child_id: str
    badge_template_id: str
    template_name: str
    description: str
    earned_at: str

    class Config:
        from_attributes = True
