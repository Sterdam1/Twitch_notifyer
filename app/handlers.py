from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from texts import message_list
from states import ChooseState, ChangeState
from aiogram.fsm.context import FSMContext
import kb
router = Router()
from sqlrequests import delete_record, insert_info, drop_table, get_col_by_col, is_tg_id, change_tg_channel, change_twitch_channel, get_tg_channels

from main import bot

@router.message(Command("start"))
async def start_handler(msg: Message):
    # await drop_table('users')
    # await drop_table('twitchers')
    await msg.delete()
    # Подумать как впихнуть data в сообщение !!
    tg_id, data = await is_tg_id(msg.chat.id)
    if tg_id:
        await msg.answer(message_list['start']['is_tg'], reply_markup=kb.menu_tg)
    else:
        await msg.answer(message_list['start']['no_tg'], reply_markup=kb.menu) #message_list['start']

@router.message(ChooseState())
async def message_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == 'ChooseState:waiting_for_channel':
        try:
            admins = await bot.get_chat_administrators(msg.text)
            admins = [a.user.id for a in admins]

            if msg.from_user.id in admins:
                await msg.answer(text=message_list['getting_chanel']['chanel_added'])
                await insert_info('users', [msg.chat.id, msg.text])
                await msg.answer(text=message_list['getting_chanel']['next_step'])
                await state.set_state(state=ChooseState.waiting_for_twitch)
            else:
                await msg.answer(text=f'{msg.from_user.username}{message_list["getting_chanel"]["error_message"]}')
            
        except Exception as e:
            await msg.answer(f"Такого канала не существует или вы еще не добавили бота в канал. { e }")

    elif cur_state == 'ChooseState:waiting_for_twitch':
        user_id = await get_col_by_col('users', 'id', 'tg_id', msg.chat.id)
        await insert_info('twitchers', [user_id, msg.text])
        await msg.answer(text=message_list['getting_twitch']['twitch_added'])
        await state.set_state(state=ChooseState.null)

@router.message(ChangeState())
async def message_handler(msg: Message, state: FSMContext):   
    cur_state = await state.get_state()  
    if cur_state == 'ChangeState:change_tg':
        try:
            admins = await bot.get_chat_administrators(msg.text)
            admins = [a.user.id for a in admins]

            if msg.chat.id in admins:
                await msg.answer(text=message_list['getting_chanel']['chanel_edited'])
                await msg.answer(f'{msg.text}, {msg.chat.id}')
                await change_tg_channel(msg.text, msg.chat.id)
        
        except Exception as e:
            await msg.answer(f'Такого канала не существует или вы еще не добавили бота в канал.')

    elif cur_state == 'ChangeState:change_twitch':
        await msg.answer(text=message_list['getting_twitch']['twitch_edited'])
        await change_twitch_channel(msg.text, msg.chat.id)

    await state.set_state(ChangeState.null)

@router.callback_query(lambda call: True)
async def call_back_handler(call: CallbackQuery, state: FSMContext):
    if call.data.split(';')[0] == 'ch':
        if call.data.split(';')[1] == 'channel':
            tg_id = await get_col_by_col('users', 'tg_id', 'tg_id', call.message.chat.id)
            if not tg_id:
                await state.set_state(state=ChooseState.waiting_for_channel)
                await call.message.answer(f'Введите название своего канала.')
            else:
                await call.message.answer("Вы уже указали канал.")
        elif call.data.split(';')[1] == 'tgchannel':
            await state.set_state(state=ChangeState.change_tg)
            await call.message.answer('Введите название нового тг канала.')
        elif call.data.split(';')[1] == 'twitchchannel':
            await state.set_state(state=ChangeState.change_twitch)
            await call.message.answer('Введите название ногово твич канала')
    
    elif call.data.split(';')[0] == 'stop':
        tg_channels = await get_tg_channels(call.message.chat.id)
        keyb = kb.gen_tg_channels(tg_channels)
        await call.message.answer(f"{message_list['stop']}", reply_markup=keyb)

    elif call.data.split(';')[1] == 'delete':
        await call.message.answer(call.data.split(';')[0])
        a = await delete_record(call.data.split(';')[0])
        await call.message.answer(str(a))
