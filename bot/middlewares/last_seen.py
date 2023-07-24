from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import Message

from services.user import UserService


class LastSeenMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        message: Message,
        data: dict[str, Any] | None = None
    ) -> Any:
        user_service: UserService = data["user_service"]
        await user_service.update_user_last_seen(message.from_user.id)
        return await handler(message, data)
