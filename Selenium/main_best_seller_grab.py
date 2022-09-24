from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


import logging
import sys

#functions
def print_product(count, product_name, asin,  rate_and_review_count, lastprice, start_price):
    print(count+')\t'+product_name[0].text[:35] + '\t' +
          asin + '\t' +
          rate_and_review_count[0].accessible_name[:4] + '\t' +
          rate_and_review_count[0].accessible_name[18:] + '\t' +
          lastprice[0].text + '\t' +
          start_price[0].text)
def get_all_product_info(url):

    driver = webdriver.Chrome()
    browser = driver.get(url)


    counter = 0
    html = driver.find_element(By.TAG_NAME, value='html')

    for i in range(9): html.send_keys(Keys.PAGE_DOWN)
    sleep(2)
    for i in range(2): html.send_keys(Keys.PAGE_DOWN)
    sleep(1)
    for i in range(2): html.send_keys(Keys.PAGE_DOWN)
    sleep(1)
    for i in range(2): html.send_keys(Keys.PAGE_DOWN)
    sleep(1)

    elements_num = driver.find_elements(By.ID, value='gridItemRoot')

    for i in (i+1 for i in range(len(elements_num))):
        try:
            start_price = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[2]/a/span/span[1]')
            lastprice = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[2]/a/span/span[2]')
            rate_and_review_count = driver.find_elements(By.XPATH,value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[1]/div/a')
            product_name = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/a[2]/span/div')
            asin = driver.find_element(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[1]/div/a').get_property('href').split('/')[4]

            print_product(str(i), product_name, asin, rate_and_review_count, start_price, lastprice)

        except:
            counter += 1
            print(str(i)+')\t\t ###\tERROR on Product\t###')

    print('-->\tNum Of Product errors: '+str(counter)+'\t<--')
    try:
        next = driver.find_element(By.XPATH, value='/html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[2]/ul/li[4]/a')

        if next.is_enabled():
            is_next_enabled = next.is_enabled()
            next_url = next.get_property('href')
            return next_url
        else:
            print('no Next Button URL == End of pages')
            return None
    except:
        print('No Next In HTML')
        return None

    driver.close()


#TODO - departments

driver = webdriver.Chrome()

urls = ['https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0',
        'https://www.amazon.com/Best-Sellers-Home-Kitchen-Bath-Products/zgbs/home-garden/1063236/ref=zg_bs_nav_home-garden_1'
        ]


# Main loop iterate between urls
for url in urls:
    x = get_all_product_info(url)
    while x is not None:
        x = get_all_product_info(x)
