from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

#functions
def print_product(count, product_name, asin,  rate_and_review_count, lastprice, start_price):
    print(count+')\t'+product_name[0].text[:25] + '\t' +
          asin + '\t' +
          rate_and_review_count[0].accessible_name[:4] + '\t\t\t' +
          rate_and_review_count[0].accessible_name[18:] + '\t\t\t' +
          lastprice[0].text + '\t\t\t' +
          start_price[0].text)
def get_all_product_info(url):

    browser = driver.get(url)
    next_url = ''
    counter = 0

    html = driver.find_element(By.TAG_NAME, value='html')

    for i in range(9): html.send_keys(Keys.PAGE_DOWN)
    sleep(1)
    for i in range(3): html.send_keys(Keys.PAGE_DOWN)
    sleep(1)
    for i in range(2): html.send_keys(Keys.PAGE_DOWN)
    sleep(2)
    for i in range(1): html.send_keys(Keys.PAGE_DOWN)

    elements_num = driver.find_elements(By.ID, value='gridItemRoot')
    try:
        next = driver.find_element(By.XPATH, value='/html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[2]/ul/li[4]/a')
    except:
        next = None

    for i in (i+1 for i in range(len(elements_num))):
        try:
            start_price = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[2]/a/span/span[1]')
            lastprice = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[2]/a/span/span[2]')
            rate_and_review_count = driver.find_elements(By.XPATH,value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[1]/div/a')
            product_name = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/a[2]/span/div')
            asin = driver.find_element(By.XPATH, value='//*[@id="gridItemRoot"]['+str(i)+']/div/div[2]/div/div[1]/div/a')
            asin = asin.get_property('href').split('/')[4]

            print_product(str(i), product_name, asin, rate_and_review_count, start_price, lastprice)

        except:
            counter += 1
            print(str(i)+')\t\t ###\tERROR on Product\t###')

    print('-->\tNum Of Product errors: '+str(counter)+'\t<--')

    if next is not None:
        next.click()
        sleep(5)
        next_url = driver.current_url
        return next_url
    else:
        print('no Next Button URL == End of pages')
        return 'no URL'





c_all = 0
driver = webdriver.Chrome()
url = 'https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0'
# url = 'https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0'


x = get_all_product_info(url)
if x is not None:
    get_all_product_info(x)
