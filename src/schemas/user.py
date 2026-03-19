from __future__ import annotations

from typing import Union
from uuid import UUID

from pydantic import ConfigDict

from src.schemas.base import BaseSchema


class UserResponse(BaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: Union[str, None]
    last_name: Union[str, None]
    email: str
    profile_pic_url: Union[str, None]
