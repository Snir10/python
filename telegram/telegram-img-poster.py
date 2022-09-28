import requests
from time import sleep
import os
import glob
def upload_to_group(img , bot, chat_id):
    file = {'photo': open(img, 'rb')}
    response = requests.post(
        'https://api.telegram.org/bot'+bot+'/sendPhoto?chat_id='+chat_id+'',
        files=file)
    return response

all_images = []
bot_id = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'
chat_id = '-1001677673014'
src_dir_path = '/Users/user/Desktop/Backup/'
folders = glob.glob(src_dir_path+'*/')

for folder in folders :
    for img in os.listdir(folder):
        sleep(2)
        resp = upload_to_group(folder+'/'+img, bot_id, chat_id)
        print(resp.status_code + '\t' + resp.text)
