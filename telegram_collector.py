from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def print_images(all_images):
    img_counter = 0
    for image in all_images:
        print("image number" + str(img_counter)+": " + image.text+"\n")
        src_attr = all_images.get_property("src")
        print("src link:" + src_attr + "\n")
        img_counter += 1


PATH = "C:\Program Files (x86)\chromedriver.exe"
print(PATH)

driver = webdriver.Chrome(PATH)

#get HTTP request
driver.get("https://web.telegram.org/#/im?p=@hypeallie")


try:
    list = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CLASS_NAME, "im_message_photo_thumb"))
    )
finally:
    print(list)
    print("posts loaded")

# all_images = driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[19]/div/div/div/div[2]/div/div[2]/div/div/a/img')
all_images = driver.find_elements_by_tag_name("img")

print_images(all_images)



print("ending.. :) :)  ")
driver.close()
driver.quit()





# reference sample of some image after loaded.
#<img class="im_message_photo_thumb" my-load-thumb="" thumb="media.photo.thumb" alt="[Photo]" width="130" height="260" src="blob:https://web.telegram.org/bd42ded1-6f5f-4488-a75b-d277920ad6b9">