from dataclasses import dataclass, field
from http import HTTPStatus
from typing import List


@dataclass
class FieldViolation:
	field: str
	message: str

@dataclass
class AppException(Exception):
	status_code: int
	message: str
	error_code: str
	success: bool = False
	
	def __post_init__(self):
		super().__init__(self.message)


@dataclass
class NotFoundError(AppException):
	status_code: int = HTTPStatus.NOT_FOUND
	message: str = "The requested resource does not exist."
	error_code: str = "RESOURCE_NOT_FOUND"


@dataclass
class ValidationError(AppException):
	status_code: int = HTTPStatus.UNPROCESSABLE_CONTENT
	message: str = "The request validation failed."
	error_code: str = "VALIDATION_ERROR"
	field_violations: List[FieldViolation] = field(default_factory=List[FieldViolation])


@dataclass
class ConflictError(AppException):
	status_code: int = HTTPStatus.CONFLICT
	message: str = "The request conflicts with current state."
	error_code: str = "CONFLICT"


@dataclass
class AuthenticationError(AppException):
	status_code: int = HTTPStatus.UNAUTHORIZED
	message: str = "Valid authentication credentials are required."
	error_code: str = "UNAUTHENTICATED"


@dataclass
class AuthorizationError(AppException):
	status_code: int = HTTPStatus.FORBIDDEN
	message: str = "You do not have permission to perform this action."
	error_code: str = "FORBIDDEN"


@dataclass
class InternalServerError(AppException):
	status_code: int = HTTPStatus.INTERNAL_SERVER_ERROR
	message: str = "Internal server error."
	error_code: str = "INTERNAL_SERVER_ERROR"

