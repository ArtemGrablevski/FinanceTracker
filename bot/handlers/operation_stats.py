from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import create_time_periods_keyboard
from services.operation import OperationService


router = Router()

@router.message(Command("incomes"))
async def cmd_incomes(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "For what time period would you like to get history of your incomes?",
        reply_markup=create_time_periods_keyboard()
    )
    await state.update_data(operation_type="income")


@router.message(Command("expenses"))
async def cmd_expenses(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "For what time period would you like to get history of your expenses?",
        reply_markup=create_time_periods_keyboard()
    )
    await state.update_data(operation_type="expense")


@router.callback_query(Text(startswith="time"))
async def operations_history_handler(
    callback: CallbackQuery,
    state: FSMContext,
    operation_service: OperationService
):
    await callback.message.delete_reply_markup()

    state_data = await state.get_data()
    operation_type: str = state_data.get("operation_type")

    period_in_days = int(callback.data.split("_")[1])

    operations = await operation_service.get_operations_for_period(
        callback.from_user.id,
        operation_type,
        period_in_days
    )

    if operations is None:
        await callback.message.answer("Operations history is empty :(")
    else:
        await callback.message.answer(operations.to_html_string())

    await state.clear()
