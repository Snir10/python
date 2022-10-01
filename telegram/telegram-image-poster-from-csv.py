import csv
import glob
import json
import os
from io import BytesIO
from time import sleep
import telethon
import requests
from PIL import Image
from telethon.types import InputSingleMedia

import telebot
import glob
import os
import telebot
from telebot.types import InputMediaPhoto, InputMediaVideo



TOKEN = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'
SEND_MEDIA_GROUP = f'https://api.telegram.org/bot{TOKEN}/sendMediaGroup'

def send_media_group(chat_id, images, caption='new message', reply_to_message_id=None):
        """
        Use this method to send an album of photos. On success, an array of Messages that were sent is returned.
        :param chat_id: chat id
        :param images: list of PIL images to send
        :param caption: caption of image
        :param reply_to_message_id: If the message is a reply, ID of the original message
        :return: response with the sent message
        """
        files = {}
        media = []
        for i, img in enumerate(images):
            with BytesIO() as output:
                try:
                    Image.open(folder_path+'/'+img).save(output, format='PNG')
                    output.seek(0)

                    name = f'photo{i}'
                    files[name] = output.read()
                    # a list of InputMediaPhoto. attach refers to the name of the file in the files dict
                    media.append(dict(type='photo', media=f'attach://{name}'))
                except:
                    print('can not open --->' + img + 'in ' + folder_name )
        media[0]['caption'] = caption
        x = requests.post(SEND_MEDIA_GROUP, data={'chat_id': chat_id, 'media': json.dumps(media), 'reply_to_message_id': reply_to_message_id }, files=files)
        return x


def upload_to_group(img , bot, chat_id):
    file = {'photo': open(img, 'rb')}
    response = requests.post(
        'https://api.telegram.org/bot'+bot+'/sendPhoto?chat_id='+chat_id+'',
        files=file)
    return response
def send_message(text, bot, chat_id):
    utl_req = 'https://api.telegram.org/bot' + bot + '/sendMessage'+'?chat_id=' + chat_id + '&text='+text
    result = requests.get(utl_req)
    print(result.text)

all_images = []
bot_id = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'

chat_id = '-1001677673014'
src_dir_path = '/Users/user/Desktop/Backup/'
folders = glob.glob(src_dir_path+'*/')
csv_path = '/Users/user/Desktop/Backup/products.csv'

with open(csv_path, 'r') as csvfile:
    datareader = csv.reader(csvfile)

    list_iterator = iter(datareader)
    next(list_iterator)

    for row in datareader:
        #message_sperator = '******************************************************************************'
        text = (
              '\nitem: ' +row[0] +
              '\nprice: '+row[1] +
              '\nlink: ' + row[2] + '-' +
              '\nae-link: ' + row[3] + '-' +
               '\nclick: ' + row[4] + '-')
        print(text
              )
        folder_name = 'Item_' +row[5]
        folder_path = src_dir_path + folder_name
        images = os.listdir(folder_path)

        images_list = []
        #
        #     images_list.append(InputSingleMedia(open(folder_path+'/'+str(img), 'rb')))

        for img in images:
            try:
                images_list.append('folder_path'+'/'+img)
            except:
                print('coould not open this file --> '+'folder_path'+'/'+img)
                pass

        y = send_media_group(chat_id=chat_id, images=images, caption=text)

        print(str(y.status_code) +'\n'+ y.text)
        sleep(3)








