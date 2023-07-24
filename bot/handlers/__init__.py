from aiogram import Dispatcher

from handlers import new_operation, operation_stats, start


def setup_handlers(dp: Dispatcher) -> None:
    dp.include_router(start.router)
    dp.include_router(operation_stats.router)
    dp.include_router(new_operation.router)
