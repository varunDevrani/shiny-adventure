from pydantic import EmailStr

from src.schemas.base import BaseSchema


class SignupRequest(BaseSchema):
    email: EmailStr
    password: str
    confirm_password: str


class LoginRequest(BaseSchema):
    email: EmailStr
    password: str


class TokenResponse(BaseSchema):
    token_type: str
    access_token: str
    refresh_token: str
