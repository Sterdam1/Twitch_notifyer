import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

import config
from texts import message_list
from handlers import router

from sqlrequests import create_tables, get_all_streamers, get_users_ids

from twitch import get_stream_info, is_stream_recently_started

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)

async def main():
    await create_tables()
    streamers = await get_all_streamers()
    users_ids = await get_users_ids()
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(check_streamers())
    # await send_patchnotes(users_ids, message_list['patchnotes'])
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
                is_diff, time_diff = await is_stream_recently_started(stream_start_time)
                if is_diff:
                    logging.info(f"{streamer_name} start streaming at {stream_start_time}")
                    await bot.send_message(chat_id=s[1], text=f'{streamer_name} начинает прямую трансляцию! \n{url}')
                else:    
                    logging.info(f"{streamer_name} streaming {time_diff}")
                
        await asyncio.sleep(300) 

async def send_patchnotes(users, message_text): #надо назвать подругому
    for id in users:
        try:
            await bot.send_message(chat_id=id, text=message_text)
        except:
            pass

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S', format='%(asctime)s - [%(levelname)s] - (%(filename)s) - %(message)s')
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever() 