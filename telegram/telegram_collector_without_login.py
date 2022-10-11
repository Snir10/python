from selenium import webdriver
from selenium.webdriver.support import ui
import pickle
PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(PATH)

"""
    Cookie can be only add to the request with same domain.
    When webdriver init, it's request url is `data:` so you cannot add cookie to it.
    So first make a request to your url then add cookie, then request you url again.
"""

options = webdriver.ChromeOptions()
options.add_argument("user-data-dir=C:\\Users\\sodedx\\AppData\\Local\\Google\\Chrome\\User Data") #Path to your chrome profile
w = webdriver.Chrome(executable_path="C:\\Users\\chromedriver.exe", chrome_options=options)

browser = driver.get('https://web.telegram.org/#/im')



print("ending.. :) :)  ")
driver.close()
driver.quit()


#C:\Users\sodedx\AppData\Local\Google\Chrome\User Data\Default


