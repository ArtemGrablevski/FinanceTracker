from typing import Literal
from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class Operation(Base):

    __tablename__ = "operations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    operation_type: Mapped[Literal["income", "expense"]]
    amount_100x: Mapped[int]
    currency: Mapped[Literal["USD", "EUR", "BYN", "PLN", "RUB", "USDT"]]
    note: Mapped[str]
    created_at: Mapped[datetime]
