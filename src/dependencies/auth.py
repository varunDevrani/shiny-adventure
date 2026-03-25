from typing import Union
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.dependencies.database import get_db
from src.errors.app_exception import AuthenticationError
from src.models.user import User
from src.utils.jwt_handler import decode_access_token


http_bearer = HTTPBearer(auto_error=False)


def get_current_user(
	credentials: Union[HTTPAuthorizationCredentials, None] = Depends(http_bearer),
	db: Session = Depends(get_db)
) -> User:
	
	if credentials is None:
		raise AuthenticationError(
			message="Authentication credentials were not provided.",
		)
	
	payload = decode_access_token(credentials.credentials)
	
	stmt = select(User).where(User.id == payload.user_id)
	user = db.scalar(stmt)
	if user is None:
		raise AuthenticationError(
			message="User associated with this token does not exist.",
			error_code="AUTH_USER_NOT_FOUND"
		)
	
	if user.deleted_at:
		raise AuthenticationError(
			message="User account is deactivated.",
			error_code="AUTH_USER_DEACTIVATED"
		)
	
	return user



