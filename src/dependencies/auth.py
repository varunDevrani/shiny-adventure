from http import HTTPStatus
from typing import Union
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.dependencies.database import get_db
from src.errors.codes import ErrorCode
from src.errors.domain_exception import DomainException
from src.models.user import User
from src.utils.jwt_handler import decode_access_token


http_bearer = HTTPBearer(auto_error=False)


def get_current_user(
	credentials: Union[HTTPAuthorizationCredentials, None] = Depends(http_bearer),
	db: Session = Depends(get_db)
) -> User:
	
	if credentials is None:
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="Invalid authentication credentials",
			error_code=ErrorCode.UNAUTHORIZED
		)
	
	payload = decode_access_token(credentials.credentials)
	
	stmt = select(User).where(User.id == payload.user_id)
	user = db.scalar(stmt)
	if user is None:
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="User no longer exists",
			error_code=ErrorCode.USER_NOT_FOUND
		)
	
	if user.deleted_at:
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="User not active",
			error_code=ErrorCode.USER_INACTIVE
		)
	
	return user



