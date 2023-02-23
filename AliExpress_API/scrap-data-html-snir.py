from time import sleep
import json

import bs4
import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

# filename="Dresses.csv"
# f=open(filename,"w")
# headers="product_ID, orders\n"
# f.write(headers)

# for p in range(1, 5):

    # my_url='https://www.aliexpress.com/category/200003482/dresses/' + str(p)+'.html?site=glo&g=y&SortType=total_tranpro_desc&needQuery=n&tag='
my_url = 'https://www.aliexpress.com/item/1005003474228451.html?spm=a2g0o.productlist.main.3.596axctbxctbGQ&algo_pvid=f11df15d-f5cf-43d8-8a47-7d83668ec173&algo_exp_id=f11df15d-f5cf-43d8-8a47-7d83668ec173-1&pdp_ext_f=%7B%22sku_id%22%3A%2212000025949310204%22%7D&pdp_npi=3%40dis%21USD%2114.53%217.99%21%21%21%21%21%40211bf3f816770957337077616d0761%2112000025949310204%21sea%21IL%21139655206&curPageLogUid=0cVtDVdM2LoK'
#had to split the above link because it did not fit on one line

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
# page_soup = soup(page_html, "html.parser")
page = bs4.BeautifulSoup(page_html, "html.parser")
# print(page.text)
count = 0
scripts = page.find_all('script')
for script in scripts:
    txt = script.text
    if txt.__contains__('tradeCount'):
        print('SUCCESS')
sleep(1)

string = scripts[16]
# x = string.contents[0]

sleep(1)



x = str(string)[-1056:-1051]
y = x[1] + x[2] + x[3] + x[4]
# print(int(y)-229)
y = y
    # last_script = script
#
# print(last_script)
# # for container in containers:
# em_order = containers.em
# try:
#     order_num = em_order.text
#
#     product_ID = containers.input["value"]
#     f.write(product_ID + "," + order_num + "\n")
#
# except:
#     print(f'no order object{containers}')
#
# f.close()