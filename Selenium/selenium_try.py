
# page link:
# https://www.amazon.com/Best-Sellers-Appliances/zgbs/appliances/ref=zg_bs_nav_0
#
# start price:
# <span class="_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z">$109.99</span>
# Last price:
# <span class="_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z">$139.99</span>

#main product div - zg-grid-general-faceout
# //*[@id="h10-asin-B0088LIINY"]/div[3]/div/a[2]/span/div
# /html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/a[2]/span/div

#/html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/a[2]/span/div

#driver.get_element_by_xpath("//div[@id='a']/div/a[@class='click']")

from selenium import webdriver
from selenium.webdriver.common.by import By


# PATH = '\Users\user\Downloads\chromedriver'
counter = 0
driver = webdriver.Chrome()
browser = driver.get('https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0')

products = [100]
rate_list=[]
price_list=[]
p_name_list=[]

prices = driver.find_elements(By.CLASS_NAME, value='_p13n-zg-list-grid-desktop_price_p13n-sc-price__3mJ9Z')
rates = driver.find_elements(By.CLASS_NAME, value='a-icon-alt')
products_name = driver.find_elements(By.CLASS_NAME, value='_p13n-zg-list-grid-desktop_truncationStyles_p13n-sc-css-line-clamp-3__g3dy1')
x = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"][1]/div/div[2]/div/div[2]/a/span/span[1]')
#print(x[0].text)
y = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"][1]/div/div[2]/div/div[2]/a/span/span[2]')
#print(y[0].text)
z = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]/div/div[2]/div/div[1]/div/a')
#print(z[0].accessible_name)
a = driver.find_elements(By.XPATH, value='//*[@id="gridItemRoot"]/div/div[2]/div/a[2]/span/div')
print(a[0].text[:25] + '\t' + z[0].accessible_name + '\t' + y[0].text + '\t' + x[0].text)



# for price in prices:
#     counter = 0
#     c_price = price.get_property('innerHTML')
#     print(str(counter)+')\t'+str(c_price))
#     price_list.insert(counter, c_price)
#     counter += 1
# for rate in rates:
#     counter = 0
#     c_rate = rate.get_property('innerHTML')
#     print(str(counter)+')\t'+str(c_rate))
#     rate_list.insert(counter, c_rate)
#     counter += 1
# for product_name in products_name:
#     counter = 0
#     c_p_name = product_name.get_property('innerHTML')
#     print(str(counter)+')\t'+str(c_p_name))
#     p_name_list.insert(counter, c_p_name)
#     counter += 1
#
# for i in range(len(p_name_list)):
#     products.insert(i, [p_name_list[i], price_list[i], rate_list[i]])






driver.close()



print('\n\nNow printing as list\n\n')
