"""Progress schemas."""

from pydantic import BaseModel


class LessonCompleteRequest(BaseModel):
    child_id: str
    lesson_id: str
    correct_answers: int
    total_attempts: int


class LessonCompleteResponse(BaseModel):
    xp_earned: int
    total_xp: int
    new_level: int
    level_up: bool
    new_streak: int
    streak_updated: bool
    badges_earned: list[str]


class LeaderboardEntry(BaseModel):
    child_id: str
    name: str
    xp_total: int
    level_number: int
    streak_current: int
    rank: int
