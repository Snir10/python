from datetime import datetime

import telethon.utils
from telethon.sync import TelegramClient
from telethon import functions, types

with TelegramClient('name', api_id, api_hash) as client:
    result = client(functions.messages.GetDialogsRequest(
        offset_date=datetime.datetime(2018, 6, 25),
        offset_id=42,
        offset_peer='username',
        limit=100,
        hash=-12398745604826,
        exclude_pinned=True,
        folder_id=42
    ))


    print(result.stringify())








