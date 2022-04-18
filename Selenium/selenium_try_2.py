from time import sleep

from furl import furl
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys




def print_product(count, product_name, asin,  rate_and_review_count, lastprice, start_price):
    print(count+')\t'+product_name[0].text[:25] + '\t' +
          asin + '\t' +
          rate_and_review_count[0].accessible_name + '\t' +
          lastprice[0].text + '\t' +
          start_price[0].text)
def get_all_product_info(url):
    browser = driver.get(url)

    html = driver.find_element(By.TAG_NAME, value='html')
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)

    sleep(1)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)

    sleep(2)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)
    html.send_keys(Keys.PAGE_DOWN)


    counter = 0
    elements_num = driver.find_elements(By.ID, value='gridItemRoot')

    for i in (i+1 for i in range(len(elements_num))):
        try:
            start_price = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[2]/a/span/span[1]')
            lastprice = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[2]/a/span/span[2]')
            rate_and_review_count = driver.find_elements(By.XPATH,value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[1]/div/a')
            product_name = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/a[2]/span/div')
            asin = driver.find_element(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[1]/div/a')

            href = asin.get_property('href')

            asin = href.split("/")


            print_product(str(i), product_name, asin[4], rate_and_review_count, start_price, lastprice)
        except:
            counter += 1
            print('###\t ERROR on Product->'+str(i)+'\t###')
    print('-->\tNum Of Product errors: '+str(counter)+'\t<--')


# PATH = '\Users\user\Downloads\chromedriver'
counter = 0
driver = webdriver.Chrome()
url = 'https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0'

get_all_product_info(url)

