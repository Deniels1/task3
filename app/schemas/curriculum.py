"""Curriculum schemas."""

from pydantic import BaseModel


class UnitResponse(BaseModel):
    id: str
    title: str
    description: str | None
    order_index: int
    published: bool

    class Config:
        from_attributes = True


class LessonResponse(BaseModel):
    id: str
    unit_id: str
    title: str
    exercise_type: str
    difficulty: int
    order_index: int
    published: bool

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: str
    lesson_id: str
    type: str
    content: str
    difficulty: int
    order_index: int

    class Config:
        from_attributes = True
