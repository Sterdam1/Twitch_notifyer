from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# callback codes:
# ch;email = choose email

menu = [
    [InlineKeyboardButton(text="Выбрать канал", callback_data="ch;channel")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
