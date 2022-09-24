

# this program collecting all asins from "BEST SELLERS" page on amazon
#this class contain amazon best sellers links
#<div role="treeitem" class="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL"><a href="/Best-Sellers-Amazon-Launchpad/zgbs/boost/ref=zg_bs_nav_0">Amazon Launchpad</a></div>
from furl import furl

from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def get_department_url(departments):
    for dep in departments:
        c = 0
        #building link string
        inner_html = dep.get_attribute('innerHTML')
        inner_html = inner_html[10::]
        title_list = inner_html.split("/")
        print(title_list[0] + "  -> DONE")
        inner_html = inner_html.split("0")
        a_link_list.insert(c, amazon_url + inner_html[0] + "0")
        c += 1

    return a_link_list

def interact_between_links(link_list):
    cc = 0
    for link in link_list:
        link = link.split("/")
        print(link)
        cc += 1
        get_asins(a_link_list[cc])
        time.sleep(2)

def get_asins(url, counter=0):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)
    asins = driver.find_elements(by=By.CLASS_NAME, value=asin_link_class)
    X = driver.find_element(by=By.XPATH, value='//*[@id="h10-asin-B074CR89QG"]/div[3]/div/a[2]')
    print(X)


    print(str(asins))

    for a in asins:
        link = a.get_attribute('href')

        f = furl(link)
        link = link.split("/")
        try:
            print(link[3]+'\t'+f.args['pd_rd_i'])
        except:
            print("An exception occurred")
        counter += 1


    driver.close()
    print('\nSUCCESS\nnumber of ASINS: ' + str(counter))

def main():
    #$$$$$$$$$$$$$$$$$$$$$$ START $$$$$$$$$$$$$$$$$$$$$$$#
    # $$$$$$$$$$$$$$$$$$$$$$ getting best seller URL $$$$$$$$$$$$$$$$$$$$$$$#
    driver.get('https://www.amazon.com/gp/bestsellers/?ref_=nav_cs_bestsellers')
    departments = driver.find_elements(by=By.CLASS_NAME, value=dep_link_class)
    # $$$$$$$$$$$$$$$$$$$$$$ building dep URL $$$$$$$$$$$$$$$$$$$$$$$#
    link_list = get_department_url(departments)
    driver.close()
    print("Finished take amazon main department")
    time.sleep(3)

    #interaction between all links
    print("now interact_between_links(link_list)")
    interact_between_links(link_list)

counter = 0
driver = webdriver.Chrome()
amazon_url = "https://www.amazon.com/"
#class for amazon best seller departments
dep_link_class = '_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf'
asin_link_class = '_p13n-zg-list-grid-desktop_style_grid-column__2hIsc'
a_link_list = []


main()


#whole grid -

#
#/html/body/div[1]/div[3]/div/div/div[1]/div/div/div[2]/div[1]/div[1]/div[1]/div/div[3]/div/a[2]