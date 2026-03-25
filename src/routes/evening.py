




from datetime import date
from http import HTTPStatus
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.dependencies.database import get_db
from src.errors.app_exception import AuthenticationError, InternalServerError, NotFoundError, ValidationError
from src.models.user import User
from src.models.evening import Evening
from src.schemas.api_response import SuccessResponse
from src.schemas.evening import EveningRequest, EveningResponse
from src.dependencies.auth import get_current_user

router = APIRouter(prefix="/evenings", tags=["Evenings"])


@router.get(
	"/{entry_date}",
	status_code=HTTPStatus.OK,
	response_model=SuccessResponse[EveningResponse],
	responses={
		ValidationError.status_code: {"model": ValidationError},
		AuthenticationError.status_code: {"model": AuthenticationError},
        NotFoundError.status_code: {"model": NotFoundError},
    }
)	
def get_evening_by_date(
	entry_date: date,
	user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
) -> SuccessResponse[EveningResponse]:
	stmt = select(Evening).where(Evening.user_id == user.id, Evening.entry_date == entry_date)
	evening = db.scalar(stmt)
	
	if evening is None:
		raise NotFoundError(
			message="Evening not found",
		)
	
	return SuccessResponse[EveningResponse](
		message=f"Evening dated[{entry_date}] fetched successfully",
		data=EveningResponse.model_validate(evening)
	)



@router.patch(
	"", 
	status_code=HTTPStatus.OK, 
	response_model=SuccessResponse[EveningResponse],
	responses={
		ValidationError.status_code: {"model": ValidationError},
		AuthenticationError.status_code: {"model": AuthenticationError},
		InternalServerError.status_code: {"model": InternalServerError}
	}
)
def update_evening_today(
	payload: EveningRequest,
	user: User = Depends(get_current_user),
	db: Session = Depends(get_db)
) -> SuccessResponse[EveningResponse]:
	stmt = select(Evening).where(Evening.user_id == user.id, Evening.entry_date == date.today())
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
		raise InternalServerError(
			message=str(exc)
		)
		
	db.refresh(evening)
	
	return SuccessResponse[EveningResponse](
		message=f"Evening dated[{date.today()}] updated successfully",
		data=EveningResponse.model_validate(evening)
	)

