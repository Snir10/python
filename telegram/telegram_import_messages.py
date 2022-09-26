import configparser
import json
import asyncio
import os
import re
from datetime import date, datetime
import telethon.sync
import logging
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)



async def main(phone):
    #log to file events
    logging.basicConfig(filename="log.txt", format="[%(asctime)s] [%(process)d] [%(levelname)s] [%(message)s]", level=logging.DEBUG)

    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = input('enter entity(telegram URL or entity id):')

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0
    json_counter = 0

    while True:
        logging.warning('Hello From Root')
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages


        msg_count = 0
        for message in messages:
            all_messages.append(message.to_dict())


            msg_content = 'no title'
            msg_content = str(message.message)


            #TODO url for print
            url = 'no url'
            price = 'no price'
            title = 'no title'
            if msg_content != '':
                url = re.search("(?P<url>https?://[^\s]+)", msg_content).group("url")
                price = str(re.findall(r"\$[^ ]+", msg_content))
                title = msg_content.split('-')[0]
                #edit price outpout
                str(price)
                price = price.split('\\')[0][2::]
                #price = price[2::]



            path = await client.download_media(message.media, "/Users/user/Desktop/Backup/")
            print('item ' + str(msg_count) +'\tlink:'+str(url)+'\tprice:'+str(price)+'\t'
                  +'Title:'+title + '\t Saved -> ', path[11::]+'\tMessage ID:' + str(message.id))  # printed after download is done

            #TODO
            #logging.info('item ' + str(msg_count) + '\tMessage ID:' + str(message.id)+title + '\t Saved -> ', path[11::])
            #logging.info('new item')
            msg_count += 1
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)

        with open('channel_messages'+str(json_counter)+'.json', 'w') as outfile:
            json.dump(all_messages, outfile, cls=DateTimeEncoder)

        outfile.close()
        json_counter += 1



        if total_count_limit != 0 and total_messages >= total_count_limit:
            break


with client:
    client.loop.run_until_complete(main(phone))