import aiohttp
import asyncio
import datetime
import pytz
import config

# client_id = "x8oc2925t0s7f4mbu5hqyri18so9ld"  # Вставьте ваш Client ID, полученный при регистрации вашего приложения на Twitch
# streamer_username = "buster"  # Имя стримера, чью трансляцию вы хотите отслеживать
# oauth_token = 'k51e937llodslz9gf7o4nc0iu1affe'

async def get_stream_info(streamer_name, client_id, oauth_token):
    url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {oauth_token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            data = await response.json()
            if data["data"]:
                return streamer_name, data["data"][0]["started_at"]
            else:
                return streamer_name, None

async def is_stream_recently_started(start_time):
    if start_time:
        stream_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
        current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        time_difference = current_time - stream_start_time
        return time_difference.total_seconds() <= 300 
    else:
        return False

# async def main():
#     while True:
#         streamer_name, stream_start_time = await get_stream_info('sterdammr', config.TWICH_CLIENT_ID, config.TWITCH_OAUTH_TOKEN)
#         if stream_start_time:
#             if await is_stream_recently_started(stream_start_time):
#                 message = f"{streamer_name} начал(а) стрим недавно."
#             else:
#                 message = f"{streamer_name} транслирует больше 5 минут."
#         else:
#             message = f"{streamer_name} оффлайн."
        
#         print(message)
        
#         await asyncio.sleep(300)  # Подождать 5 минут перед следующей проверкой

# if __name__ == "__main__":
#     asyncio.run(main())