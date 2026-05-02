"""Notifications endpoints."""

from fastapi import APIRouter

from app.schemas.notification import NotificationResponse, NotificationUpdate

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("", response_model=list[NotificationResponse])
async def get_notifications():
    """Get all notifications for current parent."""
    return [
        NotificationResponse(
            id="notif-1",
            title="Milestone!",
            message="Alice completed her first lesson!",
            notification_type="milestone",
            is_read=False,
            created_at="2024-01-15T10:00:00"
        ),
        NotificationResponse(
            id="notif-2",
            title="Streak Reminder",
            message="Alice hasn't practiced today. Keep the streak alive!",
            notification_type="streak_reminder",
            is_read=False,
            created_at="2024-01-16T18:00:00"
        )
    ]


@router.patch("/{notification_id}", response_model=NotificationResponse)
async def mark_notification_read(notification_id: str, update: NotificationUpdate):
    """Mark notification as read/unread."""
    return NotificationResponse(
        id=notification_id,
        title="Milestone!",
        message="Alice completed her first lesson!",
        notification_type="milestone",
        is_read=update.is_read,
        created_at="2024-01-15T10:00:00"
    )
