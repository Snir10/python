import requests

# /Users/user/Desktop/github projects/python/telegram

def upload_to_group(img , bot, chat_id):
    file = {'photo': open(img, 'rb')}
    response = requests.post(
        'https://api.telegram.org/bot'+bot+'/sendPhoto?chat_id='+chat_id+'',
        files=file)
    return response

group_id = '-1001677673014'
img_to_upl = '/Users/user/Desktop/github projects/python/telegram/image.png'
bot_id = '5536338381:AAGn8sPu__OmyDW3RLusbDc8BYTP0ybh7tg'
chat_id = '-1001677673014'


resp = upload_to_group(img_to_upl, bot_id, chat_id)

print(resp.status_code)
print(resp.text)
