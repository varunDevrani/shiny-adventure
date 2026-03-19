from __future__ import annotations

from pydantic import BaseModel
from pydantic import ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(
        strict=True, validate_assignment=True, extra="forbid", str_strip_whitespace=True
    )
