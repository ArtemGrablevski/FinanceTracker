import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import Settings
from db.factory import create_engine, create_sessionmaker
from handlers import setup_handlers
from middlewares import setup_middlewares


def configure_logging() -> None:
    logging.basicConfig(
        filename="bot.log",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

async def set_bot_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Restart the bot"),
            BotCommand(command="new_expense", description="Add new expense"),
            BotCommand(command="new_income", description="Add new income"),
            BotCommand(command="expenses", description="Your expenses for a certain period"),
            BotCommand(command="incomes", description="Your incomes for a certain period")
        ]
    )


async def main():

    config = Settings()

    configure_logging()

    engine = create_engine(config.postgres_dsn)
    sessionmaker = create_sessionmaker(engine)

    bot = Bot(token=config.bot_token, parse_mode="HTML")
    await set_bot_commands(bot)

    dp = Dispatcher(storage=MemoryStorage())
    setup_middlewares(dp, sessionmaker)
    setup_handlers(dp)

    await bot.delete_webhook(drop_pending_updates=True)

    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
