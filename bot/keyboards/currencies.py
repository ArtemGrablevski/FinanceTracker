from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def create_currencies_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="EUR", callback_data="currency_EUR"),
            InlineKeyboardButton(text="USD", callback_data="currency_USD"),
            InlineKeyboardButton(text="BYN", callback_data="currency_BYN")
        ],
        [
            InlineKeyboardButton(text="RUB", callback_data="currency_RUB"),
            InlineKeyboardButton(text="USDT", callback_data="currency_USDT"),
            InlineKeyboardButton(text="PLN", callback_data="currency_PLN")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
