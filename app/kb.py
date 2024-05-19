from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

# callback codes:
# ch;email = choose email

menu = [
    [InlineKeyboardButton(text="Выбрать канал", callback_data="ch;channel")],
]
# переименовать
menu_tg = [
    [InlineKeyboardButton(text="Поменять телеграмм канал", callback_data="ch;tgchannel"),
     InlineKeyboardButton(text="Поменять твич канал", callback_data="ch;twitchchannel")]
    ]

menu_tg = InlineKeyboardMarkup(inline_keyboard=menu_tg)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
