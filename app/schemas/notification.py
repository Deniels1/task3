"""Notification schemas."""

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    notification_type: str
    is_read: bool
    created_at: str

    class Config:
        from_attributes = True


class NotificationUpdate(BaseModel):
    is_read: bool
