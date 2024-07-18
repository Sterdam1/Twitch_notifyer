import aiohttp
from aiohttp import ClientConnectionError
import asyncio
import datetime
import pytz
import config
import logging
from tenacity import retry, stop_never, retry_if_exception_type


@retry(stop=stop_never, retry=retry_if_exception_type(ClientConnectionError))
async def get_stream_info(streamer_name, client_id, oauth_token):
    url = f"https://api.twitch.tv/helix/streams?user_login={streamer_name}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {oauth_token}"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                # logging.info(f"{data}")
                if data['data']:
                    if data['data'] is not []:
                        return streamer_name, data["data"][0]["started_at"]
                else:
                    # logging.info(f"{streamer_name} ne striming")
                    return streamer_name, None
    
    except Exception as e:
        print(logging.info(e))


async def is_stream_recently_started(start_time):
    if start_time:
        stream_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=pytz.utc)
        current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
        time_difference = current_time - stream_start_time
        return time_difference.total_seconds() <= 300, time_difference
    else:
        return False
