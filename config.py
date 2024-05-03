import json

with open(r'config.json') as file:
    data = json.load(file)

BOT_TOKEN = data['tg_token']