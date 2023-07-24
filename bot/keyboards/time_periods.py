from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_time_periods_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Today", callback_data="time_1"),
            InlineKeyboardButton(text="3 days", callback_data="time_3"),
            InlineKeyboardButton(text="Week", callback_data="time_7"),
            InlineKeyboardButton(text="Month", callback_data="time_30")
        ],
        [
            InlineKeyboardButton(text="3 Months", callback_data="time_90"),
            InlineKeyboardButton(text="6 months", callback_data="time_180"),
            InlineKeyboardButton(text="Year", callback_data="time_365"),
            InlineKeyboardButton(text="All time", callback_data="time_0"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)