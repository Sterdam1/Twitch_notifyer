from aiogram import  F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from texts import message_list
from states import EmailState
from aiogram.fsm.context import FSMContext
import kb

router = Router()



@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.delete()
    await msg.answer(message_list['start'], reply_markup=kb.menu)
    

@router.message()
async def message_handler(msg: Message, state: FSMContext):
    cur_state = await state.get_state()

    if cur_state == 'EmailState:waiting_for_email':
        email = msg.text
        await msg.answer(f"Ваш email: {email}")

@router.callback_query(lambda call: True)
async def call_back_handler(call: CallbackQuery, state: FSMContext):
    await state.set_state(state=EmailState.waiting_for_email)
    await call.message.answer(f'Введите email.')
