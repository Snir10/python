import os
import pathlib
from pathlib import Path
from time import sleep
from PIL import Image
from instagrapi import Client

def convertJPG(item):
    im1 = Image.open(item)
    im2 = item[:-3] + 'jpg'
    im1.save(im2)
    return im2
def convert_folder_items():
    targetDir = os.listdir(parentDir)
    orderedDir = []

    for item in targetDir:
        if item[-3:] == 'png':
            jpg_full_path = convertJPG(parentDir + item)
            orderedDir.append(pathlib.Path(jpg_full_path))
            sleep(1)
            print(orderedDir)

    print(orderedDir)
    return orderedDir



bot = Client()
bot.login(username="superhiddenbrands", password="Alma233490564")
parentDir = '/Users/user/Desktop/instagram/test/'
text = "Hello"
convertedAlbumPathList = convert_folder_items()
bot.album_upload(convertedAlbumPathList, caption=text)


