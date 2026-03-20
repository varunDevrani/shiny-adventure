


from typing import Annotated, Union
from pydantic import ConfigDict, Field
from src.schemas.base import BaseSchema


class EveningResponse(BaseSchema):
	model_config = ConfigDict(from_attributes=True)
	
	win: str
	mistake: str
	lesson_learned: str
	primary_distraction: str
	mood_rating: int
	energy_level: int


class EveningRequest(BaseSchema):
	win: Annotated[Union[str, None], Field(min_length=5, max_length=100)] = None
	mistake: Annotated[Union[str, None], Field(min_length=5, max_length=100)] = None
	lesson_learned: Annotated[Union[str, None], Field(min_length=5, max_length=100)] = None
	primary_distraction: Annotated[Union[str, None], Field(min_length=5, max_length=100)] = None
	mood_rating: Annotated[Union[int, None], Field(ge=1, le=5)] = None
	energy_level: Annotated[Union[int, None], Field(ge=1, le=5)] = None

