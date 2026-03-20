


from datetime import datetime
from typing import Union
import uuid
from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base
from src.models.mixins.id import IDMixin
from src.models.mixins.timestamp import TimestampMixin


class RefreshToken(IDMixin, TimestampMixin, Base):
	__tablename__ = "refresh_tokens"
	
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True)
	)

	token: Mapped[str] = mapped_column()
	
	expires_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True)
	)
	
	is_used: Mapped[bool] = mapped_column(
		default=False
	)
	
	device_info: Mapped[Union[str, None]] = mapped_column()


