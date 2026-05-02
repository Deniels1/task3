"""Child schemas."""

from pydantic import BaseModel


class ChildCreate(BaseModel):
    name: str
    age: int


class ChildResponse(BaseModel):
    id: str
    name: str
    age: int
    xp_total: int
    level_number: int
    streak_current: int
    streak_best: int
    lessons_completed: int

    class Config:
        from_attributes = True


class ChildProgress(BaseModel):
    child_id: str
    name: str
    xp_total: int
    level_number: int
    streak_current: int
    lessons_completed: int
    accuracy_rate: float
