import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from handlers import router

from sqlrequests import create_tables, get_all_streamers

from twitch import get_stream_info, is_stream_recently_started

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

async def main():
    await create_tables()
    streamers = await get_all_streamers()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    # asyncio.create_task(check_streamers())
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

async def check_streamers():    
    while True:
        streamers = await get_all_streamers()
        for s in streamers:
            url = s[0]
            if 'twitch.tv' in url:
                streamer_name = url.split('/')[-1]
            else:
                streamer_name = url
            # await bot.send_message(chat_id=s[1], text=streamer_name)
            streamer_name, stream_start_time = await get_stream_info(streamer_name, config.TWICH_CLIENT_ID, config.TWITCH_OAUTH_TOKEN)
            if stream_start_time:
                if await is_stream_recently_started(stream_start_time):
                    await bot.send_message(chat_id=s[1], text=f'{streamer_name} начинает прямую трансляцию! \n{url}')
        
        await asyncio.sleep(300) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())