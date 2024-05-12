import json

with open(r'config.json') as file:
    data = json.load(file)

BOT_TOKEN = data['tg_token']
TWICH_CLIENT_ID = data['twitch']['client_id']
TWITCH_OAUTH_TOKEN = data['twitch']['oauth_token']