from time import sleep
import json
import bs4
import csv
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup


url_ = 'https://wizzair.com/#/booking/select-flight/TLV/RHO/2023-04-23/2023-04-30/2/0/0/null'

from bs4 import BeautifulSoup
import requests

with requests.Session() as se:
    se.headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "en"
    }


test_sites = [
 'https://wizzair.com/#/booking/select-flight/TLV/RHO/2023-04-23/2023-04-30/2/0/0/null',
 'http://becauseimaddicted.net/',
 'http://www.lefashion.com/',
 'http://www.seaofshoes.com/',
 ]

for site in test_sites:
    # print(site)
    #get page soure
    response = se.get(site)
    # print(response)
    #print(response.text)

    import requests
    from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
r = requests.get(url_, headers=headers)
# print(r.text)


