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
                    print('coould not open this file --> '+'folder_path'+'/'+img)
                    pass

            returned_list.append(row)
        return returned_list
def sendMediaGroup(images, folder_path, caption='new message', reply_to_message_id=None):
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

        # JSON = json.dumps(media)

        resp = requests.post(SEND_MEDIA_GROUP, data={'chat_id': chat_id, 'media': json.dumps(media), 'reply_to_message_id': reply_to_message_id}, files=files, verify=False)
        sleep(int(timeout))

        return resp
def print_upload_response(resp, SUCCESS_RATE, ERROR_RATE, id, title, price, link, instaCounter):


    title = title.strip()[:20]
    title = '{:<15}'.format(title)     #make title fixed length
    if resp.status_code == 200:
        SUCCESS_RATE += 1
        x = f'[ID:{id}] [SUCCESS]' + ' ' + str(SUCCESS_RATE) + '/' + str(ERROR_RATE + SUCCESS_RATE) + '\t' +\
              title + '\t' +\
              price + '\t' +\
              link + '\t' +\
              'insta counter='+str(instaCounter)
        #print(x)
        logger.info(x)


        #TODO - save id to config #####

        # config = configparser.RawConfigParser()
        # config.read('config_files/uploader_config.ini')
        # config.set('Telegram', 'last_uploaded_id', id)
        # cfgfile = open('config_files/uploader_config.ini', 'w')
        # config.write(cfgfile, space_around_delimiters=False)  # use flag in case case you need to avoid white space.
        # cfgfile.close()
        ##########################
    elif resp.status_code == 429:
        ERROR_RATE += 1
        x = f'[ID:{id}] [FAILED]' +\
            str(SUCCESS_RATE) + '/' + str(ERROR_RATE + SUCCESS_RATE) + '\t' +\
              title + '\t' +\
              price + '\t' +\
              link + \
              ' ->ERROR CODE: 429 - please Retry send ID]' +\
              resp.text

        logger.error(x)
    else: # NOT 200 or 429
        ERROR_RATE += 1
        x = f'[ID:{id}] '+'[FAILED] ' + \
            str(ERROR_RATE) + '/' + str(ERROR_RATE + SUCCESS_RATE) +\
            title + '\t' +\
            price + '\t' +\
            link + '\t' + \
            'ERROR -> ' +\
            'status:' + str(resp.status_code) +\
             resp.text

        logger.error(x) # NOT 200

    return SUCCESS_RATE, ERROR_RATE
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
        if image[-3:] == 'jpg':
            images_path_list.append(folder_path + '/' + image)


    return [id, title, price, link, folder_path, images_path_list]
def validate_last_id(id):
    if id == c['Telegram']['last_uploaded_id']:
        logging.info(f'### arrived to dest ID: {id} ###')
        sleep(10)
        exit(0)
def print_welcome_csv_uploader(csv_path, len):
    print('##########################################################################################')
    print('###############\t\tWelcome to CSV Uploader\t\t\t\t\t\t\t\t\t##############')
    print(f'###############\t\tCSV file =>\t{csv_path[11:]}\t\t\t\t##############')
    print(f'###############\t\tItems Count =>\t{len}\t\t\t\t\t\t\t\t\t##############')
    print('##########################################################################################\n')
def logger_init():
    log = logging.getLogger('my_module_name')
    log.setLevel(level=logging.INFO)
    LOG_FORMAT = "%(log_color)s %(asctime)s %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

    fh = logging.StreamHandler()
    formatter = ColoredFormatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    fh = logging.FileHandler(f'logs/uploader_{datetime.now().strftime("%b %d, %H:%M:%S")}.log')
    fh.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s', "%Y-%m-%d %H:%M:%S"))
    fh.setLevel(logging.DEBUG)
    log.addHandler(fh)

    return log
def uploadInstagramAlbum(folder_path, text):
    logger.debug(f'starting upload to instagram')

    convertedAlbumPathList = convert_folder_items(folder_path)
    # resp = bot.album_upload(convertedAlbumPathList, caption=text, to_story=True)
    # logger.info(resp)


def uploadInstagramItem(folder_path, instaCounter):


    try:
        text_2 = 'New in Stock'
        uploadInstagramAlbum(folder_path, text_2)
        logger.info('post has successfully uploaded to instagram')
        instaCounter += 1
    except:
        logger.warning('error -> no instagram post')

    return instaCounter



def manipulate_msg_text_for_upload(csvLine, SUCCESS_RATE, ERROR_RATE, instaCounter):




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
        # manipulate price to pure float with 2 decimal digits
        if price.__contains__('$'):
            try:
                price = price.strip().replace('$', '')
                price = "{:.2f}".format(float(price))
            except:
                logger.debug('no valid price')

        price = str(price) + dollar
        text = title[:20] + '\t|\t' +  \
               price + '\n' + \
               '\nPlz Follow Images Instructions ☝🏻 \n' + \
               '\n\t🫴\t' + \
               link + '\n'
               #str(SUCCESS_RATE) + '/' + str(SUCCESS_RATE + ERROR_RATE)
        logger.debug(f'sending media group to telegram')

        resp = sendMediaGroup(images=images_path_list, folder_path=folder_path, caption=text)
        if resp.status_code == 429:
            logger.debug(f'\tID:{msg_id} [FAILED] with 429 -> RETRYING')
            sleep(10)
            resp = sendMediaGroup(images=images_path_list, folder_path=folder_path, caption=text)
        #
        # try:
        #     text_2 = 'New in Stock'
        #     uploadInstagramAlbum(folder_path, text_2)
        #     logger.info('post has successfully uploaded to instagram')
        #     instaCounter += 1
        # except:
        #     logger.warning('error -> no instagram post')

        z = print_upload_response(resp, SUCCESS_RATE, ERROR_RATE, msg_id, title, price, link, instaCounter)
        SUCCESS_RATE = z[0]
        ERROR_RATE = z[1]
        successRate = 'snir'





    else:
        ERROR_RATE += 1
        x = f'[ID:{msg_id}] [FAILED]' + str(ERROR_RATE) + '/' + str(ERROR_RATE + SUCCESS_RATE) + '\t' + \
            title + '\t' + \
            price + '\t' + \
            link + '\t' +\
            'link isnt containing s.click' + '\t\t'

        logger.warning(x)

    return [SUCCESS_RATE, ERROR_RATE, instaCounter]
def upload_product_by_id(msgID, SUCCESS_RATE, ERROR_RATE, instaCounter):
    with open(csv_path) as csv_file:
        for line in csv.DictReader(csv_file):
            if line is not None and line['id'] == msgID:
                if line['affiliate_link'][:3] == 'htt':
                    values = list(line.values())
                    csvLine = get_item(values)
                    rates = manipulate_msg_text_for_upload(csvLine, SUCCESS_RATE, ERROR_RATE, instaCounter)
                    SUCCESS_RATE = rates[0]
                    ERROR_RATE = rates[1]
                    instaCounter = rates[2]

                else:
                    title = line['title']
                    logger.warning(f'skipping no link line {title}')


    return [SUCCESS_RATE, ERROR_RATE, instaCounter]
def get_ids_from_csv():
    with open(csv_path) as csv_file:
        list_of_ids = []
        for line in csv.DictReader(csv_file):
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


#TODO - get Cred from Conf

# username = c['Telegram']['instagram_acc']
# password = c['Telegram']['instagram_pass']
# bot = Client()
# bot.login(username=username, password=password)
# bot = Client()
# bot.login(username="superhiddenbrands", password="Alma233490564")




successRate = 0
errorRate = 0

logger = logger_init()
details = open_csv()
print_welcome_csv_uploader(csv_path, len(details))


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
list_of_ids = get_ids_from_csv()
instaCounter = 0
for msg_id in list_of_ids:
    rates = upload_product_by_id(msg_id, successRate, errorRate, instaCounter)
    successRate = rates[0]
    errorRate = rates[1]
    instaCounter = rates[2]

'''     FINISH      '''
logger.info('finished')




# main()

