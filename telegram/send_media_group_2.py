import json
from io import BytesIO
import requests
from PIL import Image


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
                Image.open(img).save(output, format='PNG')
                output.seek(0)
                name = f'photo{i}'
                files[name] = output.read()
                # a list of InputMediaPhoto. attach refers to the name of the file in the files dict
                media.append(dict(type='photo', media=f'attach://{name}'))
        media[0]['caption'] = caption
        x = requests.post(SEND_MEDIA_GROUP, data={'chat_id': chat_id, 'media': json.dumps(media), 'reply_to_message_id': reply_to_message_id }, files=files)
        return x

path_list = ["/Users/user/Desktop/Backup/Item_433444/433449.png", "/Users/user/Desktop/Backup/Item_433444/433451.png",
        "/Users/user/Desktop/Backup/Item_433444/433450.png","/Users/user/Desktop/Backup/Item_433444/433452.png","/Users/user/Desktop/Backup/Item_433444/433453.png","/Users/user/Desktop/Backup/Item_433444/433444.png","/Users/user/Desktop/Backup/Item_433444/433445.png"]
images = []
chat_id = '-1001677673014'

y = send_media_group(chat_id=chat_id , images=path_list)
print(str(y.status_code) +'\n'+ y.text)