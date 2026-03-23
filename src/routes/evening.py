




from datetime import date
from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.dependencies.database import get_db
from src.errors.codes import ErrorCode
from src.errors.domain_exception import DomainException
from src.models.user import User
from src.models.evening import Evening
from src.schemas.api_response import SuccessResponse
from src.schemas.evening import EveningRequest, EveningResponse
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/evenings")


@router.get("/{entry_date}", status_code=HTTPStatus.OK, response_model=SuccessResponse[EveningResponse])
def get_evening_by_date(
	entry_date: date,
	user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
) -> SuccessResponse[EveningResponse]:
	stmt = select(Evening).where(Evening.user_id == user.id, Evening.entry_date == entry_date)
	evening = db.scalar(stmt)
	
	if evening is None:
		raise DomainException(
			status_code=HTTPStatus.NOT_FOUND,
			message="Evening not found",
			error_code=ErrorCode.EVENING_NOT_FOUND
		)
	
	return SuccessResponse[EveningResponse](
		message=f"Evening dated[{entry_date}] fetched successfully",
		data=EveningResponse.model_validate(evening)
	)



@router.patch("/{entry_date}", status_code=HTTPStatus.OK, response_model=SuccessResponse[EveningResponse])
def update_evening_by_date(
	entry_date: date,
	payload: EveningRequest,
	user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
) -> SuccessResponse[EveningResponse]:
	stmt = select(Evening).where(Evening.user_id == user.id, Evening.entry_date == entry_date)
	evening = db.scalar(stmt)
	
	if evening is None:
		evening = Evening(
			user_id=user.id,
			**payload.model_dump()
		)
		db.add(evening)
	else:
		updated_payload = payload.model_dump(exclude_none=True, exclude_unset=True)
		for key, value in updated_payload.items():
			setattr(evening, key, value)
	
	try:		
		db.commit()
	except IntegrityError as exc:
		raise DomainException(
			status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
			message=str(exc),
			error_code=ErrorCode.INTERNAL_SERVER_ERROR
		)
		
	db.refresh(evening)
	
	return SuccessResponse[EveningResponse](
		message=f"Evening dated[{entry_date}] fetched successfully",
		data=EveningResponse.model_validate(evening)
	)

