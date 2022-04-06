from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



PATH = "C:\Program Files (x86)\chromedriver.exe"
print(PATH)

driver = webdriver.Chrome(PATH)

#get HTTP request
driver.get("https://portals.aliexpress.com/")

try:
    sign_btn = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "XXX"))
    )
finally:
    sign_btn = driver.find_element_by_id("XXX")
    print(sign_btn)
    print("posts loaded")

# all_images = driver.find_element_by_xpath('//*[@id="ng-app"]/body/div[1]/div[2]/div/div[2]/div[3]/div/div[2]/div[1]/div/div[1]/div[2]/div[2]/div[19]/div/div/div/div[2]/div/div[2]/div/div/a/img')
# all_images = driver.find_elements_by_tag_name("img")