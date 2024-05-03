from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from texts import message_list

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(message_list['start'])


@router.message()
async def message_handler(msg: Message):
    await msg.answer(f"Твой ID: {msg.from_user.id}")