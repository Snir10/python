import os
import csv
import re
from time import sleep

import requests
from urllib.parse import urljoin
import logging

from aliexpress_api import AliexpressApi, models
from colorlog import ColoredFormatter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def logger_init():
    log = logging.getLogger('my_module_name')
    log.setLevel(level=logging.INFO)

    LOG_FORMAT = "%(log_color)s %(asctime)s %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

    fh = logging.StreamHandler()
    formatter = ColoredFormatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log
def createAliExpressInstance(): return AliexpressApi('34061046', '3766ae9cf22b81c88134fb56f71eb03c', models.Language.EN, models.Currency.EUR, 'sn2019')

def setAffiliateLink(next_url, no_link_recived_cnt, aliexpress):

    if next_url.startswith('https://www.aliexpress.com/item/') or next_url.startswith('https://www.aliexpress.us/item'):
        resp = aliexpress.get_affiliate_links(next_url)
        log.debug(f'AliExpress Response:\t{resp}')
        if hasattr(resp[0], 'promotion_link'):
            if resp[0].promotion_link.startswith('https'):
                affiliate_link = resp[0].promotion_link
            else:
                affiliate_link = 'Failed to convert Ali Express link\t'
                log.error(resp)
                no_link_recived_cnt += 1
        else:
            affiliate_link = 'no link from AE'
            log.error('no promotion link received from aliexpress')

    elif next_url.startswith('https://best.aliexpress.com'):
            affiliate_link = 'BROKEN: best.aliexpress.com'
    else:
        affiliate_link = 'No Ali Express link detected'
        log.warning(f'Bad link -> {next_url}')
        no_link_recived_cnt += 1
    return [affiliate_link, no_link_recived_cnt]
def download_images(album_urls, dest_fd):

    noLinkCounter = 0
    for album_index, album_url in enumerate(album_urls, 1):
        log.debug(f'Album index: {album_index}')
        album_folder = os.path.join(dest_fd, f'album_{album_index}')
        os.makedirs(album_folder, exist_ok=True)
        driver = webdriver.Chrome(service=service, options=options)

        try:
            log.debug(f'running get_album_data for album_index: {album_index}')
            get_album_data(driver, album_url, album_folder, noLinkCounter)

        except StaleElementReferenceException:
            log.error(f"Skipping album {album_index} due to stale element reference")
        driver.quit()

def get_album_data(driver, album_url, album_folder, noLinkCount):
    driver.get(album_url)

    title_div = driver.find_element(By.CSS_SELECTOR, 'span.showalbumheader__gallerytitle')
    subtitle_div = driver.find_element(By.CSS_SELECTOR, 'div.showalbumheader__gallerysubtitle.htmlwrap__main')
    image_divs = driver.find_elements(By.CSS_SELECTOR, 'div.showalbum__children.image__main')

    title = title_div.text
    subtitle_content = subtitle_div.text
    id = extract_unique_id(title)

    try: price = re.search(r'\d+(\.\d+)?\$', title).group()
    except: price = 'no price'

    link_match = re.search(r'(https?://\S+)', subtitle_content)
    if link_match:
        link = link_match.group(1)
        aff_link = setAffiliateLink(link, noLinkCount, aliexpress)[0]
    else:
        link = 'no link'
        aff_link = 'no link'

    images = []
    for i, image_div in enumerate(image_divs, 1):
        # sleep(1)
        img_tag = image_div.find_element(By.CSS_SELECTOR, 'img')
        image_url = img_tag.get_attribute('src')
        parsed_url = urljoin(album_url, image_url)

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Referer': album_url
        }

        image_name = f"image_{i}.png"

        response = requests.get(parsed_url, headers=headers)
        response.raise_for_status()

        with open(os.path.join(album_folder, image_name), 'wb') as f:
            f.write(response.content)

        images.append(image_name)

        log.debug(f"Downloaded image: {image_name}")
    log.debug(f"all images: {images}")
    log.info(f"[ID: {id}]  {title} Price: {price} \tlink: {link}\tAff-link: {aff_link}\tImages: {images.__len__()}")
def extract_unique_id(string):
    pattern = r'AN\d{4}'  # Pattern for "AN" followed by four digits

    match = re.search(pattern, string)
    if match:
        unique_id = match.group()
        return unique_id
    else:
        return 'no ID'

# Example usage:
main_urls = ["https://taozi140.x.yupoo.com/albums?page=1", "https://taozi140.x.yupoo.com/albums?page=2"]
log = logger_init()

for index, url in enumerate(main_urls):
    log.info(f'Processing URL: {url}')
    destination_folder = f'/Users/user/Desktop/yupoo_{index}'
    aliexpress = createAliExpressInstance()
    options = Options()
    options.add_argument('--headless')
    chromedriver_path = '/path/to/chromedriver'
    service = Service(chromedriver_path)
    log.debug(f"Opening main albums url: {main_urls}")
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    album_links = driver.find_elements(By.CSS_SELECTOR, 'div.showindex__children a')
    log.info(f"Albums Count: Found {album_links.__len__()} Albums !")
    album_urls = [album_link.get_attribute('href') for album_link in album_links]
    log.debug(f"Quiting main albums url: {url}")
    driver.quit()
    download_images(album_urls, destination_folder)
