import re
from typing import Literal

from pydantic import EmailStr, field_validator

from src.schemas.base import BaseSchema


PASSWORD_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$"
)

class SignupRequest(BaseSchema):
	email: EmailStr
	password: str

	@field_validator("password")
	@classmethod
	def password_strength(cls, passwd: str):
		if not PASSWORD_REGEX.fullmatch(passwd):
			raise ValueError("Password must contain uppercase, lowercase, digit, special character and be 8+ chars"
			)
		return passwd


class LoginRequest(BaseSchema):
	email: EmailStr
	password: str


class TokenResponse(BaseSchema):
    token_type: Literal["Bearer"] = "Bearer"
    access_token: str
    refresh_token: str
