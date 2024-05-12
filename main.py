import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import router

from sqlrequests import create_tables

from twitch import get_stream_info, is_stream_recently_started

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

async def main():
    await create_tables()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    
    # while True:
    #     streamer_name, stream_start_time = await get_stream_info('buster')
    #     if stream_start_time:
    #         if await is_stream_recently_started(stream_start_time):
    #             message = f"{streamer_name} начал(а) стрим недавно."
    #         else:
    #             message = f"{streamer_name} транслирует больше 5 минут."
    #     else:
    #         message = f"{streamer_name} оффлайн."
        
    #     await asyncio.sleep(300)  # Подождать 5 минут перед следующей проверкой


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())