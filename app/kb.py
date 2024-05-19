from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

menu = [
    [InlineKeyboardButton(text="Выбрать канал", callback_data="ch;channel")],
]
# переименовать
menu_tg = [
    [InlineKeyboardButton(text="Поменять телеграмм канал", callback_data="ch;tgchannel"),
     InlineKeyboardButton(text="Поменять твич канал", callback_data="ch;twitchchannel"),
     ],
     [InlineKeyboardButton(text="Прекратить рассылку", callback_data="stop;")]
    ]

def gen_tg_channels(tg_channels):
    button_layup = []
    for t in tg_channels:
        button_layup.append(InlineKeyboardButton(text=t, callback_data=f'{t};delete'))

    return InlineKeyboardMarkup(inline_keyboard=[button_layup])

menu_tg = InlineKeyboardMarkup(inline_keyboard=menu_tg)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
