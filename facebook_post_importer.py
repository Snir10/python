from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)



browser = driver.get('https://www.facebook.com/groups/alidaves2')


time.sleep(3)

#<div class="pmk7jnqg kr520xx4"
posts = driver.find_elements_by_class_name('i09qtzwb n7fi1qx3 datstx6m pmk7jnqg j9ispegn kr520xx4 k4urcfbm')


if posts != None:
    print(posts)
else:
    print("Somthing went wrong")

print("posts loaded")




    # class ="du4w35lb k4urcfbm l9j0dhe7 sjgh65i0" >