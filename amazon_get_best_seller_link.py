
# this program collecting all asins from "BEST SELLERS" page on amazon
#this class contain amazon best sellers links
#<div role="treeitem" class="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL"><a href="/Best-Sellers-Amazon-Launchpad/zgbs/boost/ref=zg_bs_nav_0">Amazon Launchpad</a></div>
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

def get_department_url(departments):
    for dep in departments:
        c = 0
        inner_html = dep.get_attribute('innerHTML')
        inner_html = inner_html[10::]
        title_list = inner_html.split("/")
        print(title_list[0] + "  -> DONE")
        inner_html = inner_html.split("0")
        a_link_list.insert(c, amazon_url + inner_html[0] + "0")
        c = c + 1
    return a_link_list
def interact_between_links(link_list):
    cc = 0
    for link in link_list:
        link = link.split("/")
        print(link[3])
        cc = cc + 1
        get_asins(a_link_list[cc])
        time.sleep(2)
    return 0
def get_asins(url):
    #PATH = "C:\Program Files (x86)\chromedriver.exe"
    driver = webdriver.Chrome(PATH)
    #browser = driver.get('https://www.amazon.com/Best-Sellers-Pet-Supplies/zgbs/pet-supplies/ref=zg_bs_nav_0')
    browser = driver.get(url)
    counter = 0
    time.sleep(5)
    asins = driver.find_elements_by_class_name('a-link-normal')

    for a in asins:
        link = a.get_attribute('href')

        f = furl(link)
        link = link.split("/")
        try:
            print(link[3]+'\t'+f.args['pd_rd_i'])
        except:
            print("An exception occurred")

        counter = counter + 1


    driver.close()
    print('\nSUCCESS\nnumber of ASINS: ' + str(counter))

PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
amazon_url = "https://www.amazon.com/"
asin_link_class = '_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf'
a_link_list = []

#$$$$$$$$$$$$$$$$$$$$$$ START $$$$$$$$$$$$$$$$$$$$$$$#
browser = driver.get('https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers')
time.sleep(3)
departments = driver.find_elements_by_class_name(asin_link_class)
time.sleep(3)
link_list = get_department_url(departments)
driver.close()
print("Finished take amazon main department")
time.sleep(3)
print("now interact_between_links(link_list)")

     ## run functions
interact_between_links(link_list)

