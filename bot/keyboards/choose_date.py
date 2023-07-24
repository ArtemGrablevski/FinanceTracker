from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_date_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="⏳ Just now", callback_data="date_now")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
