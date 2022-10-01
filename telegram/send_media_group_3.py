import json

import requests
from telethon import types
from telethon.tl.types import InputMediaPhoto
import telebot


TOKEN = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg' # token to access the HTTP API of your bot created with @BotFather
chat_id = '-1001677673014'
bot = telebot.TeleBot(token = TOKEN)
media_group = []
text = 'some caption for album'
SEND_MEDIA_GROUP = f'https://api.telegram.org/bot{TOKEN}/sendMediaGroup'



path_list = ["/Users/user/Desktop/Backup/Item_433480/433480.png", "/Users/user/Desktop/Backup/Item_433480/433481.png",
             "/Users/user/Desktop/Backup/Item_433480/433482.png", "/Users/user/Desktop/Backup/Item_433480/433483.png"]

for num in range(3):
    media_group(InputMediaPhoto(open('/Users/user/Desktop/Backup/Item_433480/'+'img%d.png' % num, 'rb')))
#bot.send_media_group(chat_id = chat_id, media = media_group)

x =  requests.post(SEND_MEDIA_GROUP, data={'chat_id': chat_id, 'media': json.dumps(media_group)},files=files)
print(x.text)