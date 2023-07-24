from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from services.operation import OperationService
from services.user import UserService


class DbServiceMiddleware(BaseMiddleware):

    def __init__(self, sessionmaker: async_sessionmaker) -> None:
        super().__init__()
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        async with self.sessionmaker() as session:
            data["operation_service"] = OperationService(session)
            data["user_service"] = UserService(session)
            return await handler(event, data)
