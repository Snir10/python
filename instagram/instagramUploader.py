import os
import pathlib
from pathlib import Path
from time import sleep

from PIL import Image

from instagrapi import Client

bot = Client()
bot.login(username="superhiddenbrands", password="Alma233490564")

# album_path = [".../Image1.jpg", ".../Image2.jpg"]

parentDir = '/Users/user/Desktop/instagram/test/'
targetDir = os.listdir(parentDir)
orderedDir = []


def convertJPG(item):
    im1 = Image.open(item)
    im2 = item[:-3] + 'jpg'
    im1.save(im2)
    return im2


for item in targetDir:
    x = item[3:]
    y = item[3::]
    z = item[-3:]
    if item[-3:] == 'png':
        jpg_path = convertJPG(parentDir + item)
        orderedDir.append(pathlib.Path(jpg_path))
        sleep(1)
        print(Path(parentDir+item))

text = "Hello"
print(orderedDir)

bot.album_upload(orderedDir, caption=text)


