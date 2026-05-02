"""Auth endpoints."""

from fastapi import APIRouter, HTTPException

from app.schemas.auth import ParentRegister, ParentLogin, TokenResponse, ParentResponse

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=ParentResponse)
async def register(data: ParentRegister):
    """Register new parent account."""
    return ParentResponse(
        id="demo-parent-id",
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        full_name=f"{data.first_name} {data.last_name}"
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: ParentLogin):
    """Login and get JWT tokens."""
    return TokenResponse(
        access_token="demo-access-token",
        refresh_token="demo-refresh-token"
    )


@router.get("/me", response_model=ParentResponse)
async def get_me():
    """Get current parent profile."""
    return ParentResponse(
        id="demo-parent-id",
        email="parent@example.com",
        first_name="John",
        last_name="Doe",
        full_name="John Doe"
    )
