from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from services.user import UserService


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, user_service: UserService):
    await state.clear()
    await message.answer(
        text=f"🚀 Hello, <b>{message.from_user.first_name}</b>!\n\n"
        "✏️ I'm a bot that will help you to <b>track</b> your <b>incomes</b> and <b>expenses</b>!\n\n"
        "🤖 <b>Available commands</b>:\n"
        "/start - Restart the bot\n"
        "/new_expense - Add new expense\n"
        "/new_income - Add new income\n"
        "/expenses - Your expenses for a certain period\n"
        "/incomes - Your incomes for a certain period\n"
    )
    await user_service.ensure_user_registration(message.from_user.id)
