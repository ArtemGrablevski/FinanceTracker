from datetime import datetime

from sqlalchemy import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from db.models.base import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, index=True)
    last_seen_at: Mapped[datetime] = mapped_column(default=datetime.now)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
