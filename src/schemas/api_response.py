


from typing import Union
from pydantic import BaseModel


class SuccessResponse[T](BaseModel):
	success: bool = True
	message: str = "Request Successful"
	data: Union[T, None] = None

