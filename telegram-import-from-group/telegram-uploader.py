import re
from io import BytesIO
import urllib3
from datetime import datetime
from colorlog import ColoredFormatter
import csv
import json
import requests
import configparser
import logging
import random
import os
import pathlib
from time import sleep
from PIL import Image
from instagrapi import Client
from time import sleep
import json

import bs4
import csv
from urllib.request import urlopen as uReq

from numpy.core.defchararray import isnumeric

''' ##### Main Functions #####

    main method Scenario
    1. open CSV
    2. print welcome
    3. create list of IDs
    4. iterate between IDs till end.

    feature request:
    add to log:
        photo IDs
        fix spaces issues
        add more error logs
        fix counters  '''

def convertJPG(item):
    im1 = Image.open(item)
    im2 = item[:-3] + 'jpg'
    im1.save(im2)
    return im2
def convert_folder_items(parentDir):
    targetDir = os.listdir(parentDir)
    orderedDir = []

    logger.debug(f'resizing images and converting to JPG')

    for item in targetDir:
        if item[-3:] == 'png':
            jpg_full_path = convertJPG(parentDir + '/' + item)

            image = Image.open(jpg_full_path)
            logger.debug(f'{item}\t image size is: {image.size}')


            image = image.convert("RGB")
            image = image.resize((1080, 1080))
            image.save(jpg_full_path)

            # image.resize(1080, 1080)
            logger.debug(f'{item}\t new image size is: {image.size}')

            orderedDir.append(pathlib.Path(jpg_full_path))
            sleep(1)
            logger.debug(f'Item to add to folder:\t {item}')

    # logger.debug(f'ordered list for instagram upload {orderedDir}')
    #mixing list - to avoid first photo with sizes
    random.shuffle(orderedDir)

    return orderedDir
def open_csv():
    returned_list = []
    with open(csv_path, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        next(iter(datareader))
        # list_iterator = next(iter(datareader))


        for row in datareader:

            item = row[0]
            price = row[1]
            link = row[4]
            folder_name = 'Item_' + row[6]
            folder_path = src_dir_path + folder_name
            id = row[6]

            images = os.listdir(folder_path)
            images_list = []

            for img in images:
                try:
                    images_list.append(folder_path+'/'+img)
                except:
                    print('could not open this file --> '+'folder_path'+'/'+img)
                    pass

            returned_list.append(row)
        return returned_list


def imagesToMedia(images, caption):
    """
    Use this method to send an album of photos. On success, an array of Messages that were sent is returned.
    chat_id: chat id
    images: list of PIL images to send
    caption: caption of image
    reply_to_message_id: If the message is a reply, ID of the original message
    response with sent message
    """
    files = {}
    media = []
    for i, img in enumerate(images):
        with BytesIO() as output:
            try:
                Image.open(img).save(output, format='PNG')
                output.seek(0)

                name = f'photo{i}'
                files[name] = output.read()
                # a list of InputMediaPhoto. attach refers to the name of the file in the files dict
                media.append(dict(type='photo', media=f'attach://{name}'))
            except:
                logger.warning(f'Please Check Image -> {img} \t in {folder_path}')
    media[0]['caption'] = caption

    return [media, files]
def sendMediaGroup(images, folder_path, caption='new message', reply_to_message_id=None):

        l = imagesToMedia(images, caption)
        media = l[0]
        files = l[1]
        # JSON = json.dumps(media)

        resp = requests.post(SEND_MEDIA_GROUP, data={'chat_id': chat_id, 'media': json.dumps(media), 'reply_to_message_id': reply_to_message_id}, files=files, verify=False)
        sleep(int(timeout))
        if resp.status_code == 429:
            logger.debug(f'ID:{msg_id} [FAILED] with 429 -> RETRYING')
            resp = sendMediaGroup(images=images_path_list, folder_path=folder_path, caption=msgTxt)
        return resp

def printStatus200(id, title, price, link, orderCount):
    orderCount = str(orderCount)
    x = f'[ID:{id}] [SUCCESS]' + ' ' + str(successRate) + '/' + str(errorRate + successRate) + '\t' +\
          title + '\t' +\
          price + '\t' +\
          link + '\t' + \
          orderCount + '\t' + \
          'insta counter='+str(instaCounter)
    logger.info(x)
def printStatus429(id, title, price, link, resp):
    x = f'[ID:{id}] [FAILED]' + \
        str(successRate) + '/' + str(errorRate + successRate) + '\t' + \
        title + '\t' + \
        price + '\t' + \
        link + \
        ' ->ERROR CODE: 429 - please Retry send ID]' + \
        resp.text

    logger.error(x)
def printStatusUnknown(id, title, price, link, resp):
    x = f'[ID:{id}] '+'[FAILED] ' + \
        str(errorRate) + '/' + str(errorRate + successRate) +\
        title + '\t' +\
        price + '\t' +\
        link + '\t' + \
        'ERROR -> ' +\
        'status:' + str(resp.status_code) +\
         resp.text

    logger.error(x) # NOT 200

def saveIdToCFG(id):
    config = configparser.RawConfigParser()
    config.read('config_files/uploader_config.ini')
    config.set('Telegram', 'last_uploaded_id', id)
    cfgfile = open('config_files/uploader_config.ini', 'w')
    config.write(cfgfile, space_around_delimiters=False)  # use flag in case case you need to avoid white space.
    cfgfile.close()
def get_item(line):
    title = line[1]
    price = str(line[2])
    link = line[5]
    folder_path = src_dir_path + 'Item_' + line[6]
    images = os.listdir(folder_path)

    id = line[6]

    images_path_list = []
    for image in images:
        if image[-3:] == 'png':
            images_path_list.append(folder_path + '/' + image)
        elif image[-3:] == 'mp4':
            images_path_list.append(folder_path + '/' + image)


    return [id, title, price, link, folder_path, images_path_list]
def validate_last_id(id):
    if id == c['Telegram']['last_uploaded_id']:
        logging.info(f'### arrived to dest ID: {id} ###')
        sleep(10)
        exit(0)
def print_welcome_csv_uploader(csv_path, len):
    now = str(datetime.today())[:-7]
    print('##########################################################################################')
    print('###############\t\tWelcome to CSV Uploader\t\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\tCSV file =>\t{csv_path[11:]}\t\t\t\t##############')
    print(f'###############\t\tItems Count =>\t{len}\t\t\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\tStarted: {now}\t\t\t\t\t\t\t##############')
    print(f'###############\t\tInstagram Flag: {instaFlag}\t\t\t\t\t\t\t\t\t##############')

    print('##########################################################################################\n')
def logger_init():
    log = logging.getLogger('my_module_name')
    if logLevel == 'DEBUG':
        log.setLevel(level=logging.DEBUG)
    else:
        log.setLevel(level=logging.INFO)

    LOG_FORMAT = "%(log_color)s %(asctime)s %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

    fh = logging.StreamHandler()
    formatter = ColoredFormatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    fh = logging.FileHandler(f'{src_dir_path}/uploader_{datetime.now().strftime("%b %d, %H-%M-%S")}.log')
    fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S"))
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)

    return log
def uploadInstagramItem(folder_path, instaCounter):
    try:
        text_2 = 'New in Stock'
        logger.debug(f'starting upload to instagram')
        convertedAlbumPathList = convert_folder_items(folder_path)
        resp = bot.album_upload(convertedAlbumPathList, caption=text_2, to_story=True, usertags=[], )
        logger.info(resp)
        logger.info('post has successfully uploaded to instagram')
        instaCounter += 1
    except:
        logger.warning('error -> no instagram post')
    return instaCounter


def createMsgTXT(title, price, link, count):
    count = str(count)
    logger.debug(f'creating a msg with: {title} {price} {link} {count}')
    if count != 'None':
        x = title[:20] + '\t|\t' + \
                 price + '\n\n' + \
                 count + '\n' + \
                 '\nPlz Follow Images Instructions ☝🏻 \n' + \
                 '\n\t🫴\t' + \
                 link + '\n'

    else:
        x = title[:20] + '\t|\t' + \
                 price + '\n' + \
                 '\nPlz Follow Images Instructions ☝🏻 \n' + \
                 '\n\t🫴\t' + \
                 link + '\n'
    return x


    # return csvLines
def get_ids_from_csv():
    with open(csv_path) as csv_file:
        list_of_ids = []
        for line in csv.DictReader(csv_file):
            if line['affiliate_link'].__contains__('click.aliexpress'):
                list_of_ids.append(str(line['id']))
    return list_of_ids



c = configparser.ConfigParser()
c.read("config_files/uploader_config.ini")

bot_id = c['Telegram']['bot_id']
SEND_MEDIA_GROUP = c['Telegram']['media_group']
chat_id = c['Telegram']['chat_id']
src_dir_path = c['Telegram']['src_dir_path']
csv_path = c['Telegram']['products_csv_path']
timeout = c['Telegram']['timeout']
#

username = c['Telegram']['instagram_acc']
password = c['Telegram']['instagram_pass']
instaFlag = c['Telegram']['uploadToInstagram']
logLevel = c['Telegram']['log_level']

# instaFlag = bool(instaFlag)

if instaFlag == 'True':
    bot = Client()
    bot.login(username=username, password=password)



successRate = 0
errorRate = 0
instaCounter = 0

logger = logger_init()
details = open_csv()
print_welcome_csv_uploader(csv_path, len(details))
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
list_of_ids = get_ids_from_csv()


def printLingOrdersCount(my_url):
    # my_url = 'https://www.aliexpress.com/item/1005003474228451.html?spm=a2g0o.productlist.main.3.596axctbxctbGQ&algo_pvid=f11df15d-f5cf-43d8-8a47-7d83668ec173&algo_exp_id=f11df15d-f5cf-43d8-8a47-7d83668ec173-1&pdp_ext_f=%7B%22sku_id%22%3A%2212000025949310204%22%7D&pdp_npi=3%40dis%21USD%2114.53%217.99%21%21%21%21%21%40211bf3f816770957337077616d0761%2112000025949310204%21sea%21IL%21139655206&curPageLogUid=0cVtDVdM2LoK'
    # my_url = 'https://he.aliexpress.com/item/1005005242644512.html'

    # had to split the above link because it did not fit on one line

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    # page_soup = soup(page_html, "html.parser")
    page = bs4.BeautifulSoup(page_html, "html.parser")
    # print(page.text)
    count = 0
    scripts = page.find_all('script')
    for script in scripts:
        txt = script.text
        if txt.__contains__('tradeCount'):
            logger.debug('tradeCount exists! we can print orders')
    sleep(1)

    string = scripts[16]
    sleep(1)

    # x = str(string)[-1056:-1051] this balance concate returns Orders: ":12,


    x = str(string)[-1056:-1051]
    # y = int(x[1] + x[2] + x[3] + x[4])

    y = x
    try:
        y = y.replace(':', '')
    except:
        logger.debug('no :')
    try:
        y = y.replace(',', '')
    except:
        logger.debug('no ,')
    try:
        y = y.replace('"', '')
    except:
        logger.debug('no "')
    try:
        y = y.replace('t', '')
    except:
        logger.debug('no t')
    try:
        y = y.replace('n', '')
    except:
        logger.debug('no t')

    x = y

    if isnumeric(x):
        if x == '0':
            logger.debug(f'numeric orders count detected: {x}')
            return None
        else:
            return f'Orders: {x}'
    else:
        return None

    #
    # orderCount = f'Orders: {x}'
    # return orderCount


for msg_id in list_of_ids:
    # rates = upload_product_by_id(msg_id, successRate, errorRate, instaCounter)
    #
    csvLines = []
    with open(csv_path) as csv_file:
        for line in csv.DictReader(csv_file):
            if line is not None and line['id'] == msg_id:
                if line['affiliate_link'][:3] == 'htt':
                    values = list(line.values())
                    csvLine = get_item(values)
                    csvLine.append(csvLines)

                    title = csvLine[1]
                    price = csvLine[2]
                    link = csvLine[3]
                    folder_path = csvLine[4]
                    images_path_list = csvLine[5]
                    msg_id = csvLine[0]
                    x = '️🧡🧡💛💛💚💚🤍🖤💜💙🤎❤️❤️❤️‍🔥️‍🔥💓💓💞💞❣️❣️💗💘💝'
                    dollar = '💲'
                    vi = '✔'
                    title += ' ' + random.choice(x)
                    if link.__contains__('click.aliexpress'):
                        if price.__contains__('$'):
                            try:
                                price = price.strip().replace('$', '')
                                price = "{:.2f}".format(float(price)) # manipulate price to pure float with 2 decimal digits
                            except:
                                logger.debug('no valid price')
                        price = str(price) + dollar


                        try:
                            orderCount = printLingOrdersCount(link)
                        except:
                            logger.warning(f'no orders count for this product')
                            orderCount = ''


                        #TODO - NEED TO BACKUP ORDER COUNT FAILED THEN TXT MSG FAIL

                        msgTxt = createMsgTXT(title, price, link, orderCount)


                        #TODO - Media Group
                        logger.debug(f'sending media group to telegram')
                        resp = sendMediaGroup(images=images_path_list, folder_path=folder_path, caption=msgTxt)

                        if instaFlag == 'True':
                            instaCounter = uploadInstagramItem(folder_path, instaCounter)


                        # TODO - prints

                        title = title.strip()[:20]
                        title = '{:<15}'.format(title)  # make title in fixed length
                        if resp.status_code == 200:
                            successRate += 1
                            printStatus200(msg_id, title, price, link, orderCount)
                        elif resp.status_code == 429:
                            errorRate += 1
                            printStatus429(msg_id, title, price, link, resp)
                        else:  # NOT 200 or 429
                            errorRate += 1
                            printStatusUnknown(msg_id, title, price, link, resp)

                    else:
                        errorRate += 1
                        x = f'[ID:{msg_id}] [FAILED]' + str(errorRate) + '/' + str(errorRate + successRate) + '\t' + \
                            title + '\t' + \
                            price + '\t' + \
                            link + '\t' + \
                            'link isn\'t containing s.click' + '\t\t'
                        logger.warning(x)
                else:
                    title = line['title']
                    logger.warning(f'skipping no link line {title}')
'''     FINISH      '''
logger.info('finished')

