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

api_hash = str(api_hash)

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
def rename_files(parent_dir, directory_name, ids_obj):
    for item in ids_obj:
        Path(parent_dir + item).rename(parent_dir + directory_name + '/' + item + '.png')



async def main(phone):
    #log to file events
    logging.basicConfig(filename="log.txt", format="[%(asctime)s] [%(process)d] [%(levelname)s] [%(message)s]", level=logging.DEBUG)
    await client.start()
    logging.debug("##\tClient Created Successfully\t##")
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

    first_id = 'first'

    #answer = input('Do you want to pull products? please type yes/no:\n')
    while True:
        msg_count = 0
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


            url = 'no'
            price = 'no'
            msg_content = 'no'
            title = 'no'

            path = '/Users/user/Desktop/Backup/'

            aliexpress = AliexpressApi('34061046', '3766ae9cf22b81c88134fb56f71eb03c', models.Language.EN,
                                       models.Currency.EUR, 'sn2019')

            msg_content = str(message.message)
            all_messages.append(message.to_dict())

            full_file_name = await client.download_media(message.media, path)
            file_id = str(message.id)
            new_file_name = path + file_id
            os.rename(full_file_name, path + file_id)
            id = str(message.id)

            with open('last_id.txt', 'r') as last_id:
                try:
                    if id == last_id.read():
                        print('id:' + id + '\t equals to last id' + last_id)
                        break
                except:
                    print('no such id exists:\t'+id)
            if msg_content != '':
                if first_id == 'first':
                    with open('last_id.txt', 'w') as last_id:
                        last_id.write(id)

                first_id = 'second'

                url = re.search("(?P<url>https?://[^\s]+)", msg_content).group("url")
                next_url = requests.get(url).url
                next_url = next_url.split('?')[0]
                if next_url.startswith('https://he.aliexpress.com/item/'):
                    affiliate_link = aliexpress.get_affiliate_links(next_url)
                    print(affiliate_link)
                    list_string = str(affiliate_link)
                    if list_string.split('/')[2] == 's.click.aliexpress.com':
                        affiliate_link = affiliate_link[0].promotion_link
                    else:
                        affiliate_link = 'no link recivied'


                print(msg_content)
                #price = str(re.findall(r"\$[^ ]+", msg_content))
                price = str(re.findall(r"\$\d+(?:\.\d+)?|\d+(?:\.\d+)?\$", msg_content))[:-2]
                title = msg_content.split('-')[0]
                parent_dir = '/Users/user/Desktop/Backup/'
                directory_name = 'Item_'+id

                # Path
                path = os.path.join(parent_dir, directory_name)
                try:
                    os.mkdir(path)
                except OSError as e:
                    if e.errno != errno.EEXIST:
                        pass

                logging.debug("Directory '%s' created" % directory_name)
                ids_obj.append(id)

                rename_files(parent_dir, directory_name, ids_obj)

                #edit price outpout
                str(price)
                price = price.split('\\')[0][2::]

                if os.path.exists('/Users/user/Desktop/Backup/products.csv'):
                    logging.debug('csv file already created -> Sending data')
                    send_msg_to_csv(title, price, url, next_url,affiliate_link, id, str(ids_obj), parent_dir+directory_name)
                else:
                    create_csv()
                    logging.debug('Creating new csv file then sending data')
                    send_msg_to_csv(title, price, url, next_url,affiliate_link, id, str(ids_obj), parent_dir+directory_name)

                print('title:' + title + '\t' +
                      'price:' + price + '\t' +
                      'link:' + url + '\t' +
                      'Message ID:' + id + '\t' +
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