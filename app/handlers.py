from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, FSInputFile
from aiogram.filters import Command
from texts import message_list
from states import ChooseState, ChangeState, FeedbackState, AdminState
from aiogram.fsm.context import FSMContext
import kb
import datetime
router = Router()
from sqlrequests import get_users_ids, get_feedback_table, delete_record, insert_info, drop_table, get_col_by_col, is_tg_id, change_tg_channel, change_twitch_channel, get_tg_channels

from main import bot, send_patchnotes

@router.message(Command("admin")) 
async def backup_handler(msg: Message):
    await msg.delete()
    if msg.chat.id == 821927308:
        await msg.answer('Выберите опцию', reply_markup=kb.admin_menu) #message_list[]

        # перенести в кол бек
        # await msg.answer_document(FSInputFile(path='db.sqlite3'))  
        # table = await get_feedback_table()
        # if table:
        #     await msg.answer(str(table))     

@router.message(Command("start", "feedback"))
async def start_handler(msg: Message, state: FSMContext):
    await msg.delete()
    tg_id, data = await is_tg_id(msg.chat.id)
    if msg.text == "/start":
        if tg_id:
            await msg.answer(message_list['start']['is_tg'], reply_markup=kb.menu_tg)
        else:
            await msg.answer(message_list['start']['no_tg'], reply_markup=kb.menu) 
    elif msg.text == '/feedback':
        await msg.answer(message_list['feedback'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button])) 
        await state.set_state(state=FeedbackState.waiting_for_feedback)

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
                await msg.answer(text=f'{msg.from_user.username}{message_list["getting_chanel"]["error_message"]}', reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
            
        except Exception as e:
            await msg.answer(f"Такого канала не существует или вы еще не добавили бота в канал. { e }", reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))

    elif cur_state == 'ChooseState:waiting_for_twitch':
        user_id = await get_col_by_col('users', 'id', 'tg_id', msg.chat.id)
        await insert_info('twitchers', [user_id, msg.text])
        await msg.answer(text=message_list['getting_twitch']['twitch_added'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
        await state.set_state(None)

@router.message(ChangeState())
async def message_handler(msg: Message, state: FSMContext):   
    cur_state = await state.get_state()  
    if cur_state == 'ChangeState:change_tg':
        try:
            admins = await bot.get_chat_administrators(msg.text)
            admins = [a.user.id for a in admins]

            if msg.chat.id in admins:
                await msg.answer(text=message_list['getting_chanel']['chanel_edited'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
                await change_tg_channel(msg.text, msg.chat.id)
                    
        except Exception as e:
            await msg.answer(f'Такого канала не существует или вы еще не добавили бота в канал.', reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))

    elif cur_state == 'ChangeState:change_twitch':
        await msg.answer(text=message_list['getting_twitch']['twitch_edited'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
        await change_twitch_channel(msg.text, msg.chat.id)

    await state.set_state(None)

@router.message(FeedbackState())
async def message_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()
    date_today = datetime.date.today().strftime('%d.%m.%Y')
    if cur_state == "FeedbackState:waiting_for_feedback":
        await msg.answer(message_list['feedback_thanks'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button])) 
        await insert_info("feedback", [msg.chat.id, msg.from_user.username, msg.text, date_today]) #datetime

    await state.set_state(None)

@router.message(AdminState())
async def message_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()
    if cur_state == 'AdminState:waiting_for_message':
        users_id = await get_users_ids()
        await send_patchnotes(users_id, msg.text)
        await msg.answer('Ваш шитпост доставлен пользователям', reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.close_button]))

@router.callback_query(lambda call: call.data.startswith('admin'))
async def call_back_handler(call: CallbackQuery, state: FSMContext):
    if call.data.split(';')[1] == 'bd':
        await call.message.answer_document(FSInputFile(path='db.sqlite3')) 
    elif call.data.split(';')[1] == 'fb':
        table = await get_feedback_table()
        if table:
            await call.message.answer(str(table))  
        else:
            await call.message.answer('Никто не оставил отзывов(',  reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.close_button]))
    elif call.data.split(';')[1] == 'send':
        await state.set_state(state=AdminState.waiting_for_message)
        await call.message.answer('Напиши сообщение, которое хочешь отправить пользователям', reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.close_button])) #message_list
    elif call.data.split(';')[1] == 'close':
        await call.message.delete()
        

@router.callback_query(lambda call: True)
async def call_back_handler(call: CallbackQuery, state: FSMContext):
    if call.data.split(';')[0] == 'new':
        if call.data.split(';')[1] == 'channel':
            tg_id = await get_col_by_col('users', 'tg_id', 'tg_id', call.message.chat.id)
            if not tg_id:
                await state.set_state(state=ChooseState.waiting_for_channel)
                await call.message.answer(f'Введите название телеграмм канала.')
            else:
                await call.message.answer("Вы уже указали канал.")
    elif call.data.split(';')[0] == 'ch':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await call.message.delete()
        if call.data.split(';')[1] == 'tgchannel':
            await state.set_state(state=ChangeState.change_tg)
            await call.message.answer('Введите название нового тг канала.', reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
        elif call.data.split(';')[1] == 'twitchchannel':
            await state.set_state(state=ChangeState.change_twitch)
            await call.message.answer('Введите название нового твич канала', reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
        elif call.data.split(';')[1] == 'stop':
            tg_channels = await get_tg_channels(call.message.chat.id)
            keyb = await kb.gen_tg_channels(tg_channels)
            await call.message.answer(f"{message_list['stop']}", reply_markup=keyb)

    elif call.data.split(';')[1] == 'delete':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await call.message.delete()
        await call.message.answer(message_list['stop_conformation'], reply_markup=InlineKeyboardMarkup(inline_keyboard=[kb.back_button]))
        a = await delete_record(call.data.split(';')[0])

    elif call.data.split(';')[0] == 'menu':
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        # await call.message.delete()
        await state.set_state(None)
        tg_id = await get_col_by_col('users', 'tg_id', 'tg_id', call.message.chat.id)
        if tg_id:
            await call.message.answer(message_list['start']['is_tg'], reply_markup=kb.menu_tg)
        else:
            await call.message.answer(message_list['start']['no_tg'], reply_markup=kb.menu)
