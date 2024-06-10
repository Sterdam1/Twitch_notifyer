import aiohttp
import asyncio
import datetime
import pytz
import config

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
