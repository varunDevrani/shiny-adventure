


from datetime import date
import uuid
from sqlalchemy import UUID
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base
from src.models.mixins.id import IDMixin
from src.models.mixins.timestamp import TimestampMixin


class Evening(IDMixin, TimestampMixin, Base):
	__tablename__ = "evenings"
	
	user_id: Mapped[uuid.UUID] = mapped_column(
		UUID(as_uuid=True)
	)
	
	entry_date: Mapped[date] = mapped_column(
		default=lambda: date.today()
	)
	
	win: Mapped[str] = mapped_column()
	
	mistake: Mapped[str] = mapped_column()
	
	lesson_learned: Mapped[str] = mapped_column()
	
	primary_distraction: Mapped[str] = mapped_column()
	
	mood_rating: Mapped[int] = mapped_column()
	
	energy_level: Mapped[int] = mapped_column()
	
