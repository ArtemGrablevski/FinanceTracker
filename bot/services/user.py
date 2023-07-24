from datetime import datetime

from sqlalchemy import select, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User


class UserService:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def _is_user_registered(self, user_id: int) -> bool:
        user = await self.session.scalar(
            select(User).where(User.id == user_id)
        )
        return user is not None

    async def _create_user(self, user_id: int) -> None:
        await self.session.execute(
            insert(User).values(id=user_id)
        )
        await self.session.commit()

    async def ensure_user_registration(self, user_id: int) -> None:
        is_user_registered = await self._is_user_registered(user_id)
        if not is_user_registered:
            await self._create_user(user_id)

    async def update_user_last_seen(self, user_id: int) -> None:
        await self.session.execute(
            update(User).where(User.id == user_id).values(last_seen_at=datetime.now())
        )
        await self.session.commit()
