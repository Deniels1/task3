"""API v1 router."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, children, units, lessons, leaderboard, exercises, badges, notifications, admin

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(auth.router)
api_v1_router.include_router(children.router)
api_v1_router.include_router(units.router)
api_v1_router.include_router(lessons.router)
api_v1_router.include_router(exercises.router)
api_v1_router.include_router(badges.router)
api_v1_router.include_router(leaderboard.router)
api_v1_router.include_router(notifications.router)
api_v1_router.include_router(admin.router)
