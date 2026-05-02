"""Auth schemas."""

from pydantic import BaseModel, EmailStr


class ParentRegister(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class ParentLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class ParentResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    full_name: str

    class Config:
        from_attributes = True
