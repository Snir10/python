import configparser
import errno
import json
import os
import os.path
import re
import csv
from aliexpress_api import AliexpressApi, models

import logging
import requests
from pathlib import Path
from datetime import date, datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)



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

#api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']



# Create the client and connect
client = TelegramClient(username, api_id, api_hash)
def send_msg_to_csv(title, price, link, nexturl,affiliate_link, id, images, path):
    with open('/Users/user/Desktop/Backup/products.csv', 'a', encoding='UTF8', newline='') as f:
        data = [title, price, link, nexturl,affiliate_link, id, images, path]
        writer = csv.writer(f)
        writer.writerow(data)
def create_csv():
    with open('/Users/user/Desktop/Backup/products.csv', 'x', encoding='UTF8', newline='') as f:
        header = ['title', 'price', 'link','next url','affiliate_link',  'id', 'images', 'path']
        writer = csv.writer(f)
        writer.writerow(header)
def rename_and_move_files(parent_dir, directory_name, ids_obj):
    for item in ids_obj:
        Path(parent_dir + item).rename(parent_dir + directory_name + '/' + item + '.png')


def get_message_details(msg_content):
    price = str(re.findall(r"\$\d+(?:\.\d+)?|\d+(?:\.\d+)?\$", msg_content))[:-2]
    title = msg_content.split('-')[0]
    price = price.split('\\')[0][2::]

    url = re.search("(?P<url>https?://[^\s]+)", msg_content).group("url")
    next_url = requests.get(url).url.split('?')[0]
    if next_url.startswith('https://he.aliexpress.com/item/'):
        aliexpress = AliexpressApi('34061046', '3766ae9cf22b81c88134fb56f71eb03c', models.Language.EN,
                                   models.Currency.EUR, 'sn2019')
        affiliate_link = aliexpress.get_affiliate_links(next_url)
        list_string = str(affiliate_link)
        if list_string.split('/')[2] == 's.click.aliexpress.com':
            affiliate_link = affiliate_link[0].promotion_link
        else:
            affiliate_link = 'no link received'
    else:
        affiliate_link = 'no link received'

    return [title, price, url, next_url, affiliate_link]


async def main(phone):
    await client.start()
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    #me = await client.get_me()

    entity = 'https://t.me/hypeallie'
    my_channel = await client.get_entity(entity)
    offset_id = 0
    limit = 100
    all_messages = []
    total_messages = 0
    total_count_limit = 0
    json_counter = 0
    ids_obj = []

    first_id = 0
    first_id_flag = False

    msg_count = 0

    while True:
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

                for message in messages:


                    path = '/Users/user/Desktop/Backup/'
                    id = str(message.id)
                    msg_content = str(message.message)
                    new_file_name = path + id


                    all_messages.append(message.to_dict())

                    full_file_name = await client.download_media(message.media, path)

                    os.rename(full_file_name, path + id)


                    if msg_content != '':

                        details = get_message_details(msg_content)

                        title = details[0]
                        price = details[1]
                        url = details[2]
                        next_url = details[3]
                        affiliate_link = details[4]

                        parent_dir = '/Users/user/Desktop/Backup/'
                        directory_name = 'Item_'+id

                        path = os.path.join(parent_dir, directory_name)
                        try:
                            os.mkdir(path)
                        #fix for file already exists
                        except OSError as e:
                            if e.errno != errno.EEXIST:
                                pass

                        ids_obj.append(id)

                        rename_and_move_files(parent_dir, directory_name, ids_obj)



                        if os.path.exists('/Users/user/Desktop/Backup/products.csv'):
                            send_msg_to_csv(title, price, url, next_url,affiliate_link, id, str(ids_obj), parent_dir+directory_name)
                        else:
                            create_csv()
                            send_msg_to_csv(title, price, url, next_url,affiliate_link, id, str(ids_obj), parent_dir+directory_name)

                        print(str(datetime.now()) + '\t' +
                              'ID:' + id + '\t' +
                              'title:' + title + '\t' +
                              'price:' + price + '\t' +
                              'link:' + url + '\t' +
                              'aff_link:' + affiliate_link + '\t' +
                              'Saved-> ' + new_file_name + '\t' +
                              'Folder IDs:' + str(ids_obj))
                        msg_count += 1
                        ids_obj = []

                    else:
                        ids_obj.append(id)
                        offset_id = messages[len(messages) - 1].id
                        total_messages = len(all_messages)

                        json_counter += 1

                        if total_count_limit != 0 and total_messages >= total_count_limit:
                            break

with client:
    client.loop.run_until_complete(main(phone))