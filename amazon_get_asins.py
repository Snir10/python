
# this program collecting all asins from "BEST SELLERS" page on amazon
import selenium
import html
from furl import furl

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
def get_asins(url):
    PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)

#    browser = driver.get('https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0')
    browser = driver.get(url)

    counter = 0
    time.sleep(5)
    #<div class="sc-cVUNPX doNspm">B09K8M96MD</div>
    #<div class="pmk7jnqg kr520xx4"
    asins = driver.find_elements_by_class_name('a-link-normal')

    for a in asins:
        link = a.get_attribute('href')
        f = furl(link)
        print(f.args['pd_rd_i'])
        counter = counter+1

    print('\nnumber of ASINS: '+str(counter))

