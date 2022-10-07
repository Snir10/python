from io import BytesIO
from time import sleep
from PIL import Image
import glob
import os
import csv
import json
import requests
from datetime import datetime

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

def open_csv(csv_path):
    returned_list = []
    with open(csv_path, 'r') as csvfile:
        datareader = csv.reader(csvfile)
        list_iterator = next(iter(datareader))
        for row in datareader:

            item = row[0]
            price = row[1]
            link = row[4]
            folder_name = 'Item_' +row[5]
            folder_path = src_dir_path + folder_name

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
def send_media_group(chat_id, images, folder_path, caption='new message', reply_to_message_id=None):
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
                    Image.open(img).save(output, format='PNG')
                    output.seek(0)

                    name = f'photo{i}'
                    files[name] = output.read()
                    # a list of InputMediaPhoto. attach refers to the name of the file in the files dict
                    media.append(dict(type='photo', media=f'attach://{name}'))
                except:
                    print('ERROR: can not open -->' + img + 'in ' + folder_path)
        media[0]['caption'] = caption
        x = requests.post(SEND_MEDIA_GROUP, data={'chat_id': chat_id, 'media': json.dumps(media), 'reply_to_message_id': reply_to_message_id }, files=files)
        return x
def print_upload_response(resp, SUCCESS_RATE, ERROR_RATE, title, price, link ):
    time = datetime.now()

    # print statuses to logger
    if resp.status_code == 200:
        SUCCESS_RATE += 1
        print(str(time)+'\tItems:' + str(SUCCESS_RATE) + '/' + str(ERROR_RATE + SUCCESS_RATE) + '\t' +'\t' + 'SUCCESS' + '\t'+'\t'+
              title + '\t' +
              price + '\t' +
              link + '\t')
    else:
        ERROR_RATE += 1
        print(str(time)+'\t'+title + '\t' +
              price + '\t' +
              link + '\t'+
              'Uploading ISSUE -> ' +
              'status:' + str(resp.status_code) +
              'error: ' + resp.text + str(ERROR_RATE) + '/' + str(ERROR_RATE + SUCCESS_RATE))
    return SUCCESS_RATE, ERROR_RATE

def get_item(details):
    title = details[0]
    price = str(details[1])
    link = details[4]
    folder_path = src_dir_path + 'Item_' + details[5]
    images = details[6].split(',')

    images_path_list = []

    # image path list filler
    for image in images:
        images_path_list.append(folder_path + '/' + image.split('\'')[1] + '.png')


    return [title, price, link, folder_path, images_path_list]


bot_id = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'
SEND_MEDIA_GROUP = f'https://api.telegram.org/bot{bot_id}/sendMediaGroup'
chat_id = '-1001677673014'
src_dir_path = '/Users/user/Desktop/Backup/'
folders = glob.glob(src_dir_path+'*/')
csv_path = '/Users/user/Desktop/Backup/products.csv'
SUCCESS_RATE = 0
ERROR_RATE = 0

title = ''
price = ''
link = ''
images = []

details = open_csv(csv_path)




for i in range(len(details)):
    list_of_product_details = []
    list_of_product_details = get_item(details[i])

    title = list_of_product_details[0]
    price = list_of_product_details[1]
    link = list_of_product_details[2]
    folder_path = list_of_product_details[3]
    images_path_list = list_of_product_details[4]




    #caption text to send
    text = title+'\U0001f600'+'\n'+price+'\n'+link+'\n'+'SUCCESS RATE: '+str(SUCCESS_RATE) +' FROM '+str(SUCCESS_RATE+ERROR_RATE)


    resp = send_media_group(chat_id=chat_id, images=images_path_list,folder_path=folder_path,caption=text)


    if resp.status_code == 429:
        print(resp.text)


    z = print_upload_response(resp, SUCCESS_RATE, ERROR_RATE, title, price, link)
    SUCCESS_RATE = z[0]
    ERROR_RATE = z[1]
    sleep(40)








