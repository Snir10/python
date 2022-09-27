import configparser
import json
import os
import os.path
import re
import csv
import requests
from pathlib import Path

from datetime import date, datetime
import logging
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)


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





def send_msg_to_csv(title, price, link, nexturl, id, images, path):

    with open('/Users/user/Desktop/Backup/products.csv', 'a', encoding='UTF8', newline='') as f:
        data = [title, price, link, nexturl, id, images, path]
        writer = csv.writer(f)
        writer.writerow(data)
def create_csv():
    with open('/Users/user/Desktop/Backup/products.csv', 'x', encoding='UTF8', newline='') as f:
        header = ['title', 'price', 'link','next url', 'id', 'images', 'path']
        writer = csv.writer(f)
        writer.writerow(header)







async def main(phone):
    #log to file events
    logging.basicConfig(filename="log.txt", format="[%(asctime)s] [%(process)d] [%(levelname)s] [%(message)s]", level=logging.DEBUG)

    await client.start()
    print("##\tClient Created Successfully\t##")
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
    ids_obj = []

    #answer = input('Do you want to pull products? please type yes/no:\n')
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

            msg_content = 'no'
            msg_content = str(message.message)


            url = 'no'
            price = 'no'
            title = 'no'



            path = '/Users/user/Desktop/Backup/'
            full_file_path = await client.download_media(message.media, path)
            filename = full_file_path
            file_id = str(message.id)
            new_file_name = path + file_id
            os.rename(filename, path + file_id)

            id = str(message.id)

            if msg_content != '':
                url = re.search("(?P<url>https?://[^\s]+)", msg_content).group("url")
                next_url = requests.get(url).url
                next_url = next_url.split('?')[0]
                price = str(re.findall(r"\$[^ ]+", msg_content))
                title = msg_content.split('-')[0]

                parent_dir = '/Users/user/Desktop/Backup/'
                directory_name = 'Item_'+id


                # Path
                path = os.path.join(parent_dir, directory_name)
                os.mkdir(path)
                print("Directory '%s' created" % directory_name)

                ids_obj.append(id)


                #put images into folder
                for item in ids_obj:
                    Path(parent_dir+item).rename(parent_dir+directory_name+'/'+item+'.png')

                #edit price outpout
                str(price)
                price = price.split('\\')[0][2::]

                if os.path.exists('/Users/user/Desktop/Backup/products.csv'):
                    send_msg_to_csv(title, price, url, next_url, id, str(ids_obj), parent_dir+directory_name)
                else:
                    create_csv()
                    send_msg_to_csv(title, price, url, next_url, id, str(ids_obj), parent_dir+directory_name)

                #ids_obj.append(id)
                #print('\n' + str(ids_obj))

                print('item ' + str(msg_count) + '\t' +
                      'title:' + title + '\t' +
                      'price:' + price + '\t' +
                      'link:' + url + '\t' +
                      'Saved-> ' + new_file_name + '\t' +
                      'Message ID:' + id + '\t' +
                      'Folder IDs:' + str(ids_obj))

                msg_count += 1
                ids_obj = []

            else:
                ids_obj.append(id)






        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)

        #with open('channel_messages'+str(json_counter)+'.json', 'w') as outfile:
            #json.dump(all_messages, outfile, cls=DateTimeEncoder)

        #outfile.close()
        json_counter += 1



        if total_count_limit != 0 and total_messages >= total_count_limit:
            break


with client:
    client.loop.run_until_complete(main(phone))