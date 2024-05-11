import requests
import time
import datetime
import pytz


client_id = "x8oc2925t0s7f4mbu5hqyri18so9ld"  # Вставьте ваш Client ID, полученный при регистрации вашего приложения на Twitch
streamer_username = "follentass"  # Имя стримера, чью трансляцию вы хотите отслеживать
oauth_token = 'k51e937llodslz9gf7o4nc0iu1affe'


def check_stream_status():
    url = f"https://api.twitch.tv/helix/streams?user_login={streamer_username}"
    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {oauth_token}"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data["data"]:
            return data["data"][0]['started_at']
    except Exception as e:
        print("Error occurred:", e)
        return False, None

def is_stream_recently_started(start_time):
    if start_time:
        stream_start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%SZ")  # Парсинг времени в формат datetime
        current_time = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)  # Текущее время с информацией о смещении
        stream_start_time = stream_start_time.astimezone(pytz.utc)  # Привести время начала стрима к UTC
        time_difference = current_time - stream_start_time
        return time_difference.total_seconds() <= 300  # 300 секунд = 5 минут

def main():
    while True:
        stream_start_time = check_stream_status()
        if stream_start_time:
            if is_stream_recently_started(stream_start_time):
                print(f"{streamer_username} начал(а) стрим недавно.")
            else:
                print(f"{streamer_username} не транслирует.")
        else:
            print(f"{streamer_username} оффлайн.")
        
        time.sleep(60)   # Проверяем статус стрима каждую минуту

if __name__ == "__main__":
    main()