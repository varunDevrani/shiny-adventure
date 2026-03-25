


from http import HTTPStatus
from fastapi import APIRouter, Depends

from src.dependencies.auth import get_current_user
from src.models.user import User
from src.schemas.api_response import SuccessResponse
from src.schemas.user import UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", status_code=HTTPStatus.OK, response_model=SuccessResponse[UserResponse])
def get_user(
	user: User = Depends(get_current_user)
) -> SuccessResponse[UserResponse]:
	return SuccessResponse[UserResponse](
		message="User fetched successfully",
		data=UserResponse.model_validate(user)
	)


