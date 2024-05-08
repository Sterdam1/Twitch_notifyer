from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from texts import message_list
from states import ChooseState
from aiogram.fsm.context import FSMContext
import kb
router = Router()
from sqlrequests import insert_info, drop_table, get_col_by_col
from main import bot

@router.message(Command("start"))
async def start_handler(msg: Message):
    # await drop_table('users')
    # await drop_table('twitchers')
    await msg.delete()
    await msg.answer(message_list['start'], reply_markup=kb.menu) #message_list['start']

    
@router.message(ChooseState())
async def message_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == 'ChooseState:waiting_for_channel':
        try:
            # надо сделать так чтобы если такой канал уже есть в базе,
            # то можно было обновить только админу который его записал
            await msg.answer(text=f"Ваш канал записан")
            await insert_info('users', [msg.chat.id, msg.text])
            await msg.answer(text="Напишите твич канал чтобы получать уведомления о стримах.")
            await state.set_state(state=ChooseState.waiting_for_twitch)
        except Exception as e:
            await msg.answer(f"Такого канала не существует или вы еще не добавили бота в канал. { e }")
    elif cur_state == 'ChooseState:waiting_for_twitch':
        # прописать try когда я разберусь с твич апи
        user_id = await get_col_by_col('users', 'id', 'tg_id', msg.chat.id)
        await insert_info('twitchers', [user_id, msg.text])
        
@router.callback_query(lambda call: True)
async def call_back_handler(call: CallbackQuery, state: FSMContext):
    if call.data == 'ch;channel':
        tg_id = await get_col_by_col('users', 'tg_id', 'tg_id', call.message.chat.id)
        if not tg_id:
            await state.set_state(state=ChooseState.waiting_for_channel)
            await call.message.answer(f'Введите название своего канала.')
        else:
            # Надо сделать кнопку редактирования канала и добавления twitch
            await call.message.answer("Вы уже указали канал.")
