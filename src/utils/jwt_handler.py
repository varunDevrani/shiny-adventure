from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from uuid import UUID

import jwt
from pydantic import BaseModel

from src.core.config import settings
from src.errors.codes import ErrorCode
from src.errors.domain_exception import DomainException

ALGORITHM = "HS256"


class AccessTokenPayload(BaseModel):
	user_id: UUID
	iat: int
	exp: int


def create_access_token(user_id: UUID) -> str:
	current_time = datetime.now(timezone.utc)
	expire_time = current_time + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

	payload = AccessTokenPayload(
		user_id=user_id,
		iat=int(current_time.timestamp()),
		exp=int(expire_time.timestamp())
	)

	return jwt.encode(payload.model_dump(mode="json"), settings.JWT_SECRET_KEY, ALGORITHM)


def decode_access_token(token: str) -> AccessTokenPayload:
	try:
		raw: dict = jwt.decode(token, settings.JWT_SECRET_KEY, [ALGORITHM])
	except jwt.ExpiredSignatureError:
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="Token has expired",
			error_code=ErrorCode.TOKEN_EXPIRED
		)
	except jwt.InvalidTokenError:
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="Token is invalid",
			error_code=ErrorCode.TOKEN_INVALID
		)

	return AccessTokenPayload(**raw)
