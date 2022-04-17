
# page link:
# https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_nav_0
#
# start price:
# <span class="_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z">$109.99</span>
# Last price:
# <span class="_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z">$139.99</span>


from selenium import webdriver
from selenium.webdriver.common.by import By


# PATH = '\Users\user\Downloads\chromedriver'
counter = 0
driver = webdriver.Chrome()
browser = driver.get('https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0')

startprice = driver.find_elements(By.CLASS_NAME, value='_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z')

for price in startprice:
    counter += 1
    current_price = price.get_property('innerHTML')
    print(str(counter)+')\t'+str(current_price))

driver.close()