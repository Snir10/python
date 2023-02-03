import configparser
import errno
import json
import os
import os.path
import re
import csv
from time import sleep
from aliexpress_api import AliexpressApi, models
import logging
import requests
from pathlib import Path
from datetime import date, datetime
from colorlog import ColoredFormatter
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)

###
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)

# Reading Configs
config = configparser.ConfigParser()
config.read("config_files/importer_config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

phone = config['Telegram']['phone']
username = config['Telegram']['username']
conf_id = config['Telegram']['importer_last_id']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

#NOT IN USE
def validate_last_id(id, conf_id):
    if conf_id == id:
        logging.info(f'### arrived to dest ID: {id} ###')
        logging.info(f'### SUCCESSFULLY DONE {id} ###')
        logging.info(f'###  {id} ###')
        logging.info(f'### arrived to dest ID: {id} ###')

        sleep(20)
        exit(0)
def validate_black_list(string):
    if string.__contains__('https://hypeallie.online/jackzhang/'):
        return True

#CSV FUNCTIONS
def send_msg_to_csv(message_time, csv_f_name, title, price, link, nexturl, affiliate_link, id, images, parent, dir_name):
    with open(parent+csv_f_name, 'a', encoding='UTF8', newline='') as f:
        data = [message_time, title, price, link, nexturl,affiliate_link, id, images, parent+dir_name]
        writer = csv.writer(f)
        writer.writerow(data)
def create_csv(path, name):
    with open(path + name, 'x', encoding='UTF8', newline='') as f:
        header = ['uploaded time', 'title', 'price', 'link','next url','affiliate_link',  'id', 'images', 'path']
        writer = csv.writer(f)
        writer.writerow(header)

#Files HANDALING
def rename_and_move_files(handle_fd, parent_dir, directory_name, ids_obj):
    for item in ids_obj:
        Path(handle_fd + item).rename(parent_dir + directory_name + '/' + item + '.png')
def add_item_images_folder(parent_dir, directory_name):
    path = os.path.join(parent_dir, directory_name)
    try:
        os.mkdir(path)
    # fix for file already exists
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
def create_handling_folder(parent_dir, param):
    path = os.path.join(parent_dir, param)

    try:
        os.mkdir(path)
    # fix for file already exists
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass

#GET MSG TEXT
def get_message_details(msg_content, vl_no_link_count):
    price = str(re.findall(r"\$\d+(?:\.\d+)?|\d+(?:\.\d+)?\$", msg_content))[:-2]
    title = msg_content.split('-')[0]
    price = price.split('\\')[0][2::]
    price = price.replace('$', '')
    price = price+'$'

    url = re.search("(?P<url>https?://[^\s]+)", msg_content).group("url")
    next_url = requests.get(url).url.split('?')[0]
    if next_url.startswith('https://he.aliexpress.com/item/'):
        aliexpress = AliexpressApi('34061046',
                                   '3766ae9cf22b81c88134fb56f71eb03c',
                                   models.Language.EN,
                                   models.Currency.EUR, 'sn2019')
        affiliate_link = aliexpress.get_affiliate_links(next_url)
        list_string = str(affiliate_link)
        if list_string.split('/')[2] == 's.click.aliexpress.com':
            affiliate_link = affiliate_link[0].promotion_link
        else:
            affiliate_link = 'Failed to convert Ali Express link'
            vl_no_link_count +=1
    elif next_url.startswith('https://best.aliexpress.com'):
            affiliate_link = 'BROKEN: best.aliexpress.com'
    else:
        affiliate_link = 'No Ali Express link detected'
        vl_no_link_count += 1

    sleep(2)

    return [title, price, url, next_url, affiliate_link, vl_no_link_count]

#LOG HANDALING
def print_to_log(id, title, price, url, affiliate_link, new_file_name, ids_obj, img_count):

    title = title.strip()[:18]
    title = '{:<15}'.format(title)


    if affiliate_link.startswith('https://s.click.ali'):
        status = '[SUCCESS]'
    else:
        status = '[FAILED]'

    x = status + '\t' + \
        f'[ID: {id}]  ' \
        f'Title: {title} \t' +\
        'Price:' + price + '\t' +\
        'Link:' + url + '\t' +\
        'Aff_link:' + affiliate_link + '\t' +\
        'Saved-> ' + new_file_name + '\t' +\
        'Images files:' + str(ids_obj) + '\t' +\
        'img count: '+str(img_count)


    if affiliate_link.startswith('https://s.click.ali'):
        logger.info(x)
    else:
        logger.error(x)
def print_welcome_csv_importer(f_name):
    print('##########################################################################################')
    print('###############\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t##############')
    print('###############\t\tWelcome to CSV Importer\t\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\tCSV file =>\t{f_name}\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\twill FINISH importing until -> ID:{conf_id}\t\t\t\t##############')
    print('###############\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t##############')
    print(f'##########################################################################################')
def logger_init():
    # init logger
    logger = logging.getLogger('my_module_name')
    logger.setLevel(level=logging.INFO)
    LOG_FORMAT = "%(log_color)s %(asctime)s %(levelname)-6s%(reset)s | %(log_color)s%(message)s%(reset)s"

    fh = logging.StreamHandler()
    formatter = ColoredFormatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    fh = logging.FileHandler(f'logs/importer_{datetime.now().strftime("%b %d, %H:%M:%S")}.log')
    fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S"))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    return logger


#MAIN FOLDER
async def main(phone, last_main_msg=None, first_try=True):

    await client.start()
    # Ensure you're authorized - was ->    if await client.is_user_authorized() == False: !!!
    if not await client.is_user_authorized():
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
    ids_obj = []


    msg_count = 0
    img_counter = 0
    no_link_recived_cnt = 0



    handle_fd = config['Telegram']['handle_fd']
    csv = config['Telegram']['csv']
    parent_dir = config['Telegram']['parent_dir']

#real day
    path = os.path.join(parent_dir)

    try:
        os.mkdir(path)
    # fix for file already exists
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass

##
    #parent_dir = path




    create_handling_folder(parent_dir, 'products_handaling')
    print_welcome_csv_importer(csv)



    while True:

        print("\n|| Current Offset ID is:", offset_id, "|| Total Messages:", total_messages, "|| Msg counter:", msg_count, "|| No link count:", no_link_recived_cnt, ' ||\n')
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
            sleep(0.15)

            all_messages.append(message.to_dict())
            id = str(message.id)
            #
            # if id == '484428':
            #     pass



            if message.message == '':
                full_file_name = await client.download_media(message.media, parent_dir)
                img_counter += 1
                ids_obj.append(id)

                try:
                    os.rename(full_file_name, handle_fd + id)
                except:
                    logger.info(f'full_file_name: {full_file_name}, handle_fd: {handle_fd}, id: {id}')



            #txt msg only
            else:
                #txt message + handling is conatin photos + NOT first try
                if os.listdir(handle_fd):

                    #open folder for new id
                    id = str(message.id)
                    last_id = str(last_main_msg.id)
                    directory_name = 'Item_' + last_id

                    add_item_images_folder(parent_dir, directory_name)
                    rename_and_move_files(handle_fd, parent_dir, directory_name, ids_obj)





                    # handaling text to log and csv
                    message_time = str(message.date.strftime("%b %d, %H:%M:%S"))
                    try:
                        details = get_message_details(message.message, no_link_recived_cnt)
                    except:
                        details = ['no title', 'no title', 'no title', 'no title', 'no title', 'no title']
                    title = details[0]
                    price = details[1]
                    url = details[2]
                    next_url = details[3]
                    affiliate_link = details[4]
                    no_link_recived_cnt = details[5]

                    if os.path.exists(parent_dir + csv):
                        send_msg_to_csv(message_time, csv, title, price, url, next_url, affiliate_link, id,
                                        str(ids_obj), parent_dir, directory_name)
                    else:
                        create_csv(parent_dir, csv)
                        send_msg_to_csv(message_time, csv, title, price, url, next_url, affiliate_link, id,
                                        str(ids_obj), parent_dir, directory_name)

                    new_file_name = ''

                    print_to_log(id, title, price, url, affiliate_link, new_file_name, ids_obj, img_counter)


                    ids_obj = []
                    first_try = False



                    last_main_msg = message


                else:
                    # reinit counters and objects
                    last_main_msg = message


                    img_counter = 0
                    msg_count += 1
                    directory_name = 'Item_'+id

                    #first photo and txt
                    full_file_name = await client.download_media(message.media, parent_dir)
                    msg_content = str(message.message)
                    new_file_name = parent_dir + id
                    add_item_images_folder(parent_dir, directory_name)



                    ids_obj.append(id)

                    try:
                        os.rename(full_file_name, handle_fd + id)
                    except:
                        logger.info(f'full_file_name: {full_file_name}, handle_fd: {handle_fd}, id: {id}')
                # full_file_name = await client.download_media(message.media, parent_dir)

            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)

            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
with client:
    logger = logger_init()
    client.loop.run_until_complete(main(phone))