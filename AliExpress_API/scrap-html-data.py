import bs4
import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename="Dresses.csv"
f=open(filename,"w")
headers="product_ID, orders\n"
f.write(headers)

for p in range(1, 5):

    my_url='https://www.aliexpress.com/category/200003482/dresses/' + str(p)+'.html?site=glo&g=y&SortType=total_tranpro_desc&needQuery=n&tag='
    #had to split the above link because it did not fit on one line

    uClient = uReq(my_url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    containers = page_soup.findAll("div",{"class":"item"})


for container in containers:
    em_order = container.em
    try:
        order_num = em_order.text

        product_ID = container.input["value"]
        f.write(product_ID + "," + order_num + "\n")

    except:
        print(f'no order object{container}')

f.close()