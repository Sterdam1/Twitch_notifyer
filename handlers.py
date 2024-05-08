from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from texts import message_list
from states import ChooseState
from aiogram.fsm.context import FSMContext
import kb
router = Router()
from sqlrequests import insert_info, drop_table
from main import bot

@router.message(Command("start"))
async def start_handler(msg: Message):
    await drop_table('users')
    await drop_table('twitchers')
    await msg.delete()
    await msg.answer(message_list['start'], reply_markup=kb.menu) #message_list['start']

    
@router.message(ChooseState())
async def message_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == 'ChooseState:waiting_for_channel':
        channel = msg.text
        await msg.answer(f'Вы написали вот такое имя канала {channel}')
        await bot.send_message(chat_id=msg.text, text=f"Ваш канал записан")

        # await insert_info('users', [msg.chat.id, ])


        
@router.callback_query(lambda call: True)
async def call_back_handler(call: CallbackQuery, state: FSMContext):
    if call.data == 'ch;channel':
        await state.set_state(state=ChooseState.waiting_for_channel)
        await call.message.answer(f'Введите название своего канала.')
