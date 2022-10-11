from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

PATH = "C:\Program Files (x86)\chromedriver.exe"
print(PATH)

driver = webdriver.Chrome(PATH)

#get HTTP request
driver.get("https://www.aliexpress.com")

#Print Title to Console
print(driver.title)

search = driver.find_element_by_id("search-key")
search.send_keys("case")
search.send_keys(Keys.RETURN)

try:
    list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "list-items"))
    )
    print('finished to wait 10 seconds, list-items has been uploaded')

finally:
    print("done")

list = driver.find_element_by_class_name("list-items")
print(list.text)




#    driver.quit()

#time.sleep(5)


# close specific Tab browser
#driver.close()


# close whole browser
# driver.quit()

