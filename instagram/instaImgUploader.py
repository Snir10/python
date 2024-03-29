from instabot import Bot
import os
import shutil


def clean_up():
    dir = "config"
    remove_me = "imgs\img.jpg.REMOVE_ME"
    # checking whether config folder exists or not
    if os.path.exists(dir):
        try:
            # removing it because in 2021 it makes problems with new uploads
            shutil.rmtree(dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    if os.path.exists(remove_me):
        src = os.path.realpath("imgs\img.jpg")
        os.rename(remove_me, src)


def upload_post():
    bot = Bot()

    bot.login(username="superhiddenbrands", password="Alma233490564")
    bot.upload_photo(["/Users/user/Desktop/482547.png"], caption="SUCCESS_2")
    bot.upload_story_photo("/Users/user/Desktop/instagram/482548.png")



if __name__ == '__main__':
    clean_up()
    upload_post()