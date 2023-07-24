from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards import create_currencies_keyboard, create_date_keyboard
from services.operation import OperationService
from states.new_operation import NewOperationState
from utils.parser import parse_operation_info_message, parse_datetime_message


router = Router()

@router.message(Command("new_income"))
async def cmd_new_income(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="💸 Please, choose the currency!",
        reply_markup=create_currencies_keyboard()
    )
    await state.update_data(operation_type="income")


@router.message(Command("new_expense"))
async def cmd_new_expense(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="💸 Please, choose the currency!",
        reply_markup=create_currencies_keyboard()
    )
    await state.update_data(operation_type="expense")


@router.callback_query(Text(startswith="currency"))
async def currency_chosen_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete_reply_markup()

    currency = callback.data.split("_")[1]
    await state.update_data(currency=currency)

    await callback.message.answer(
        text="🔥 Great! When was the operation performed? "
        "Send me date in the format <i>16:33 01.12.23</i> or <i>01.12.23</i>",
        reply_markup=create_date_keyboard())
    await state.set_state(NewOperationState.waiting_for_operation_date)


@router.callback_query(Text(text="date_now"))
async def date_from_callback_chosen_handler(callback: CallbackQuery, state: FSMContext):

    await callback.message.delete_reply_markup()

    state_data = await state.get_data()
    if state_data.get("date") is not None:
        return await callback.answer()

    await state.update_data(date=datetime.now())
    await callback.message.answer(
        "💰 Finally, send me message in format <i>170 supermarket</i>!"
    )
    await state.set_state(NewOperationState.waiting_for_operation_info)


@router.message(NewOperationState.waiting_for_operation_date)
async def date_chosen_handler(message: Message, state: FSMContext):

    if message.text is None:
        return await message.answer("Invalid message. Please, try again!")

    try:
        date = parse_datetime_message(message.text)
    except ValueError:
        return await message.answer(
            text="Invalid message format! "
            "Correct format is <i>16:33 01.12.23</i> or <i>01.12.23</i>\n"
            "Please, try again!"
        )

    await state.update_data(date=date)
    await message.answer(
        "💰 Finally, send me message in format <i>48 supermarket</i>!"
    )
    await state.set_state(NewOperationState.waiting_for_operation_info)


@router.message(NewOperationState.waiting_for_operation_info)
async def operation_info_chosen_handler(
    message: Message,
    state: FSMContext,
    operation_service: OperationService
):
    if message.text is None:
        return await message.answer("Invalid message. Please, try again!")

    try:
        operation_info = parse_operation_info_message(message.text)
    except ValueError:
        return await message.answer(
            "Invalid message format. Example: <b>18 shop</b>. Please, try again :)"
        )

    state_data = await state.get_data()
    operation_type = state_data.get("operation_type")
    currency = state_data.get("currency")
    operation_date = state_data.get("date")

    await operation_service.create_operation(
        user_id=message.from_user.id,
        operation_type=operation_type,
        amount=operation_info.amount,
        currency=currency,
        note=operation_info.note,
        created_at=operation_date
    )

    await message.answer(f"😎 Successfully saved new {operation_type}!")
    await state.clear()
