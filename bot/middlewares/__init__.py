from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from middlewares.db_service import DbServiceMiddleware
from middlewares.last_seen import LastSeenMiddleware


def setup_middlewares(dp: Dispatcher, sessionmaker: async_sessionmaker) -> None:
    dp.message.outer_middleware(DbServiceMiddleware(sessionmaker))
    dp.callback_query.middleware(DbServiceMiddleware(sessionmaker))
    dp.message.middleware(LastSeenMiddleware())
    dp.callback_query.middleware(LastSeenMiddleware())
