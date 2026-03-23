import secrets
from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import APIRouter, Depends, Request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import func, select

from src.core.config import settings
from src.dependencies.database import get_db
from src.errors.codes import ErrorCode
from src.errors.domain_exception import DomainException
from src.models.refresh_token import RefreshToken
from src.models.user import User
from src.schemas.api_response import SuccessResponse
from src.schemas.auth import AuthRequest, TokenResponse
from src.schemas.user import UserResponse
from src.utils.hash import hash_password, verify_password
from src.utils.jwt_handler import create_access_token


router = APIRouter(prefix="/auth")


@router.post("/signup", status_code=HTTPStatus.CREATED, response_model=SuccessResponse[UserResponse])
def signup(
	payload: AuthRequest,
	db: Session = Depends(get_db)
) -> SuccessResponse[UserResponse]:
	stmt = select(User).where(User.email == payload.email)
	user = db.execute(stmt).scalar_one_or_none()
	if user is not None:
		raise DomainException(
			status_code=HTTPStatus.CONFLICT,
			message="User with email already exists",
			error_code=ErrorCode.USER_ALREADY_EXISTS
		)

	new_user = User(
		email=payload.email,
		password_hash=hash_password(payload.password)
	)
	db.add(new_user)
	try:
		db.commit()
	except IntegrityError:
		raise DomainException(
			status_code=HTTPStatus.CONFLICT,
			message="User with email already exists",
			error_code=ErrorCode.USER_ALREADY_EXISTS
		)
	db.refresh(new_user)

	return SuccessResponse[UserResponse](
		message="User created successfully. Please login",
		data=UserResponse.model_validate(new_user)
	)


@router.post("/login", status_code=HTTPStatus.OK, response_model=SuccessResponse[TokenResponse])
def login(
	payload: AuthRequest,
	request: Request,
	db: Session = Depends(get_db)
) -> SuccessResponse[TokenResponse]:
	stmt = select(User).where(User.email == payload.email)
	user = db.execute(stmt).scalar_one_or_none()
	if user is None:
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="Invalid email or password",
			error_code=ErrorCode.UNAUTHORIZED
		)

	if not verify_password(user.password_hash, payload.password):
		raise DomainException(
			status_code=HTTPStatus.UNAUTHORIZED,
			message="Invalid email or password",
			error_code=ErrorCode.UNAUTHORIZED
		)

	active_sessions_stmt = select(func.count()).where(RefreshToken.user_id == user.id, RefreshToken.is_used == False, RefreshToken.expires_at > datetime.now(timezone.utc))
	active_sessions_count = db.scalar(active_sessions_stmt) or 0

	if active_sessions_count >= settings.MAX_SESSION_PER_USER:
		oldest_stmt = select(RefreshToken).where(RefreshToken.user_id == user.id, RefreshToken.is_used == False, RefreshToken.expires_at > datetime.now(timezone.utc)).order_by(RefreshToken.created_at.asc()).limit(1)
		oldest_token = db.scalar(oldest_stmt)

		if oldest_token is not None:
			db.delete(oldest_token)

	access_token = create_access_token(user.id)
	refresh_token = secrets.token_urlsafe(32)
	device_info = request.headers.get("User-Agent")

	new_refresh_token = RefreshToken(
		user_id=user.id,
		token=refresh_token,
		expires_at=datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
		device_info=device_info
	)
	db.add(new_refresh_token)
	try:
		db.commit()
	except IntegrityError:
		raise DomainException(
			status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
			message="Internal server error",
			error_code=ErrorCode.INTERNAL_SERVER_ERROR
		)

	tokens = TokenResponse(
		access_token=access_token,
		refresh_token=refresh_token
	)

	return SuccessResponse[TokenResponse](
		message="User logged in successfully",
		data=tokens
	)
