import requests
from time import sleep
import os
import glob
import csv

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
        product_content = ('******************************************************************************' +
              '\nitem: ' +row[0] +
              '\nprice: '+row[1] +
              '\nlink: ' + row[2] + '-' +
              '\nae-link: ' + row[3] + '-' )
        folder_name = 'Item_' +row[4]
        folder_path = src_dir_path + folder_name
        images = os.listdir(folder_path)

        for img in images:
            sleep(2)
            resp = upload_to_group(src_dir_path + folder_name +'/'+ img, bot_id, chat_id)
            print(str(resp.status_code) + '\t' + resp.text)

        sleep(3)
        #TODO add functionallty to add photos before
        send_message(product_content, bot_id, chat_id)




