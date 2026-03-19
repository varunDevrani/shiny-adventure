from typing import Union

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.models.base import Base
from src.models.mixins.id import IDMixin
from src.models.mixins.timestamp import TimestampMixin


class User(IDMixin, TimestampMixin, Base):
    __tablename__ = "users"

    first_name: Mapped[Union[str, None]] = mapped_column()

    last_name: Mapped[Union[str, None]] = mapped_column()

    email: Mapped[str] = mapped_column()

    profile_pic_url: Mapped[Union[str, None]] = mapped_column()

    is_verified: Mapped[bool] = mapped_column(default=False)
