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
from datetime import datetime
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
#CSV File
def send_msg_to_csv(message_time, csv_f_name, title, price, link, nexturl, affiliate_link, id, images, parent, dir_name, msgContent):
    with open(parent+csv_f_name, 'a', encoding='UTF8', newline='') as f:
        data = [message_time, title, price, link, nexturl, affiliate_link, id, images, parent+dir_name, msgContent]
        writer = csv.writer(f)
        writer.writerow(data)
def create_csv(path, name):
    with open(path + name, 'x', encoding='UTF8', newline='') as f:
        header = ['uploaded time', 'title', 'price', 'link', 'next url', 'affiliate_link',  'id', 'images', 'path', 'msg content']
        writer = csv.writer(f)
        writer.writerow(header)
#Rename and Move
def renameAndMoveFiles(directory_name, ids_obj):

    #TODO - IF ITEM IS *.MP4 - to handle it as video.

    for item in ids_obj:
        try:
            if item[len(item) - 3:] == 'mp4':
                Path(handle_fd + item).rename(parent_dir + directory_name + '/' + item + '.mp4')
            else:
                Path(handle_fd + item).rename(parent_dir + directory_name + '/' + item + '.png')

        except:
            logger.error(f'Cannot move from{handle_fd + item} to {parent_dir + directory_name}')
#Create Folders
def createItemDirectory(directory_name):
    path = os.path.join(parent_dir, directory_name)
    try:
        os.mkdir(path)
    # fix for file already exists
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
def createTempImgFolder(param):
    path = os.path.join(parent_dir, param)

    try:
        os.mkdir(path)
    # fix for file already exists
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
#Get Msg TXT
def getTitle(msg_content):
    try:
        title = msg_content.split('-')[0]
    except:
        logger.error(f'problem with title: -> {msg_content}')
        title = 'error'
    return title


def getPrice(msg_content):
    try:
        price = str(re.findall(r"\$\d+(?:\.\d+)?|\d+(?:\.\d+)?\$", msg_content))[:-2]
        price = price.split('\\')[0][2::]
        price = price.replace('$', '')
        #print(price)
        price = ('%.2f' % float(price))
        #print(str(price))
    except:
        logger.error('price NOT detected')
        price = ''
    return price+'$'
def getURL(msg_content):
    try:
        url = re.search("(?P<url>https?://[^\s]+)", msg_content).group("url")
    except:
        url = ('no url detected')
    return url
#TODO - TBD
# def setAffiliateLink():
#     pass
def getNextURL(url):
    try:
        x = requests.get(url).url.split('?')[0]
    except:
        x = 'no url'
    return x
def setAffiliateLink(next_url, no_link_recived_cnt, aliexpress):

    if next_url.startswith('https://he.aliexpress.com/item/'):
        resp = aliexpress.get_affiliate_links(next_url)
        logger.debug(resp)
        if hasattr(resp[0], 'promotion_link'):
            if resp[0].promotion_link.startswith('https'):
                affiliate_link = resp[0].promotion_link
            else:
                affiliate_link = 'Failed to convert Ali Express link\t'
                logger.error(resp)
                no_link_recived_cnt += 1
        else:
            affiliate_link = 'no link from AE'
            logger.error('no promotion link received from aliexpress')

    elif next_url.startswith('https://best.aliexpress.com'):
            affiliate_link = 'BROKEN: best.aliexpress.com'
    else:
        affiliate_link = 'No Ali Express link detected'
        no_link_recived_cnt += 1
    return [affiliate_link, no_link_recived_cnt]
#LOG Handling
def print_to_log(id, title, price, url, affiliate_link, new_file_name, ids_obj, img_count, msg_time, last_msg):

    title = title.strip()[:18]
    title = '{:<15}'.format(title)


    if affiliate_link.startswith('https://s.click.ali'):
        status = '[SUCCESS]'
    else:
        status = '[FAILED]'

    x = status + '\t' + \
        f'[ID: {id}]  ' \
        f'Uploaded in: {msg_time} \t' +\
        f'Title: {title} \t' +\
        'Price:' + price + '\t' +\
        'Link:' + url + '\t' +\
        'Aff_link:' + affiliate_link + '\t' +\
        'Saved-> ' + new_file_name + '\t' +\
        'Image files:' + str(ids_obj) + '\t' +\
        'img count: '+str(img_count)
         # f'last_msg: {last_msg[:-1]}'


    if affiliate_link.startswith('https://s.click.ali'):
        logger.info(x)
    else:
        logger.error(x)
def print_welcome_csv_importer(csvFileName):
    print('##########################################################################################')
    print('###############\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t##############')
    print('###############\t\tWelcome to CSV Importer\t\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\tCSV file =>\t{csvFileName}\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\twill FINISH importing until -> ID:\t\t\t\t##############')
    print('###############\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t##############')
    print(f'##########################################################################################')
def logger_init():
    # init logger
    logger = logging.getLogger('my_module_name')
    logger.setLevel(level=logging.INFO)
    LOG_FORMAT = "%(log_color)s %(asctime)s %(levelname)-6s%(reset)s | %(log_color)s%(message)s%(reset)s"

    # logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S', filename='/Users/user/Desktop/Backup/importer_log.log', filemode='w')

    fh = logging.StreamHandler()
    formatter = ColoredFormatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    fh = logging.FileHandler(f'logs/importer_{datetime.now().strftime("%b %d, %H:%M:%S")}.log')
    fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S"))
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    return logger
#Config Handling
def initalConfig():
    # Reading Configs
    config.read("config_files/importer_config.ini")

    # Setting configuration values
    api_id = config['Telegram']['api_id']
    api_hash = config['Telegram']['api_hash']

    phone = config['Telegram']['phone']
    username = config['Telegram']['username']

    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)

    return [client, phone]
#Create Folder
def createParentDir():
    path = os.path.join(parent_dir)

    try:
        os.mkdir(path)
    # fix for file already exists
    except OSError as e:
        if e.errno != errno.EEXIST:
            pass
def createAliExpressInstance():
    return AliexpressApi('34061046',
                               '3766ae9cf22b81c88134fb56f71eb03c',
                               models.Language.EN,
                               models.Currency.EUR, 'sn2019')
def sendMsgInfoToCSV(messageTime, csvFile, title, price, url, next_url, affiliate_link, last_id, ids_obj, parent_dir,
                     directory_name, msgContent):
    if os.path.exists(parent_dir + csvFile):
        send_msg_to_csv(messageTime, csvFile, title, price, url, next_url, affiliate_link, last_id,
                        str(ids_obj), parent_dir, directory_name, msgContent)
    else:
        create_csv(parent_dir, csvFile)
        send_msg_to_csv(messageTime, csvFile, title, price, url, next_url, affiliate_link, last_id,
                        str(ids_obj), parent_dir, directory_name, msgContent)
def renameImg(full_file_name, id):
    try:
        if full_file_name[len(full_file_name) - 3 : ] == 'mp4':
            logger.info(f'mp4 detected {full_file_name}')
            try:
                os.rename(full_file_name, handle_fd + id + '.mp4')
            except:
                logger.info(f'full_file_name: {full_file_name}, handle_fd: {handle_fd}, id: {id}')
        else:
            try:
                os.rename(full_file_name, handle_fd + id)
            except:
                logger.info(f'full_file_name: {full_file_name}, handle_fd: {handle_fd}, id: {id}')
    except:
        logger.error(f'couldn\'t rename a file:  {full_file_name}')
def getMsgUploadedDate(message):
    return str(message.date.strftime("%b %d, %H:%M:%S"))
def calculateSuccessRate(main_msg_id_counter, no_link_recived_cnt):
    try:
        affLinkCount = main_msg_id_counter - no_link_recived_cnt
        x = (affLinkCount / main_msg_id_counter) * 100
        return str(round(x, 2)) + '%'
    except:
        logger.error('failed to calculate success rate')
        return 'error'


async def main(phone, last_main_msg=None):
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
    main_msg_id_counter = 0
    msg_count = 0
    img_counter = 0
    no_link_recived_cnt = 0
    affLinkCount = 0
    successRate = '0.00%'

    print_welcome_csv_importer(csvFile)
    createParentDir()
    createTempImgFolder('products_handaling')

    aliexpress = createAliExpressInstance()

    while True:
        print("\n|| Current Offset ID is:", offset_id, "|| Total Messages:", total_messages, "|| Msg counter:",
              main_msg_id_counter, '|| Affiliate links', str(affLinkCount), "|| Failed Links:", no_link_recived_cnt,'|| SUCESS_RATE', str(successRate), '\n')
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



            all_messages.append(message.to_dict())
            id = str(message.id)


            #photo or video only
            if message.message == '': # MSG with photo only
                full_file_name = await client.download_media(message.media, parent_dir)
                img_counter += 1
                ids_obj.append(id)
                renameImg(full_file_name, id)
            else: # txt msg + photo
                main_msg_id_counter += 1
                if os.listdir(handle_fd): #txt message + handling is conatin photos
                    id = str(message.id)
                    try:
                        last_id = str(last_main_msg.id)
                    except:
                        logger.warning('no last msg found')
                    directory_name = 'Item_' + last_id


                    createItemDirectory(directory_name)
                    renameAndMoveFiles(directory_name, ids_obj)
                    messageTime = getMsgUploadedDate(message)

                    title = getTitle(last_main_msg.message)
                    price = getPrice(last_main_msg.message)
                    url = getURL(last_main_msg.message)
                    next_url = getNextURL(url)

                    resp = setAffiliateLink(next_url, no_link_recived_cnt, aliexpress)

                    affiliate_link = resp[0]
                    no_link_recived_cnt = resp[1]


                    #TODO fix calculation
                    successRate = calculateSuccessRate(main_msg_id_counter, no_link_recived_cnt)
                    sendMsgInfoToCSV(messageTime, csvFile, title, price, url, next_url, affiliate_link, last_id,
                                    str(ids_obj), parent_dir, directory_name, last_main_msg.message)
                    new_file_name = ''
                    img_counter += 1
                    print_to_log(last_id, title, price, url, affiliate_link, new_file_name, ids_obj, img_counter, messageTime, last_main_msg.message)
                    ids_obj = []
                    full_file_name = await client.download_media(message.media, parent_dir)
                    renameImg(full_file_name, id)
                    ids_obj.append(id)
                    img_counter = 0
                    last_main_msg = message

                else: # handle fd empty + txt message = first message
                    logger.info('first message?')

                    ids_obj.append(id)
                    last_main_msg = message
                    img_counter = 0
                    msg_count += 1
                    full_file_name = await client.download_media(message.media, parent_dir)
                    renameImg(full_file_name, id)
                    createItemDirectory('Item_'+id)

            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break
config = configparser.ConfigParser()
list = initalConfig()
client = list[0]
phone = list[1]
with client:
    logger = logger_init()
    #TODO - parent dir globally - erase parent dir from functions
    parent_dir = config['Telegram']['parent_dir']
    handle_fd = config['Telegram']['handle_fd']
    csvFile = config['Telegram']['csv']
    client.loop.run_until_complete(main(phone))