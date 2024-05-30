from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import asyncio

menu = [
    [InlineKeyboardButton(text="Выбрать канал", callback_data="new;channel")],
]
# переименовать
menu_tg = [
    [InlineKeyboardButton(text="Поменять телеграмм", callback_data="ch;tgchannel"),
     InlineKeyboardButton(text="Поменять твич", callback_data="ch;twitchchannel"),
     ],
     [InlineKeyboardButton(text="Прекратить рассылку", callback_data="ch;stop")]
    ]

back_button = [InlineKeyboardButton(text='Вернуться в меню', callback_data=f'menu;')]

async def gen_tg_channels(tg_channels):
    button_layup = []
    for t in tg_channels:
        button_layup.append(InlineKeyboardButton(text=t, callback_data=f'{t};delete'))

    return InlineKeyboardMarkup(inline_keyboard=[button_layup, back_button])

menu_tg = InlineKeyboardMarkup(inline_keyboard=menu_tg)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
