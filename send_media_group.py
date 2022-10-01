from telethon.tl import types, functions
from telethon.tl.types import InputMediaPhoto
from telegram import InputMediaPhoto

def upload_media_group():
    chat_id = -1001677673014
    TOKEN = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'
    bot = telebot.TeleBot(TOKEN)
    vid_media = []
    path_list = ["/Users/user/Desktop/Backup/Item_433480/433480.png", "/Users/user/Desktop/Backup/Item_433480/433481.png",
            "/Users/user/Desktop/Backup/Item_433480/433482.png","/Users/user/Desktop/Backup/Item_433480/433483.png"]

    for filename in path_list:
        print('read:', filename)
        with open(filename, 'rb') as fh:
            data = fh.read()
            media = InputMediaPhoto(data)
            vid_media.append(media)

    bot.send_message(chat_id, "Sending media group...")
    bot.send_media_group(chat_id, vid_media)

upload_media_group()