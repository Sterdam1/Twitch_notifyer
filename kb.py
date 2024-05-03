from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# callback codes:
# ch;email = choose email

menu = [
    [InlineKeyboardButton(text="Выбрать email", callback_data="ch;email")],
]
menu = InlineKeyboardMarkup(inline_keyboard=menu)
