import os
import csv
import re

import requests
from urllib.parse import urljoin
import logging

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
    log.setLevel(level=logging.DEBUG)

    LOG_FORMAT = "%(log_color)s %(asctime)s %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"

    fh = logging.StreamHandler()
    formatter = ColoredFormatter(LOG_FORMAT)
    fh.setFormatter(formatter)
    log.addHandler(fh)

    return log

def download_images(album_urls, destination_folder):
    csv_file = os.path.join(destination_folder, 'album_data.csv')
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f)
        if f.tell() == 0:  # Check if the file is empty
            writer.writerow(['ID', 'Title', 'Subtitle Content', 'Link', 'Images'])
        else:
            f.seek(0, os.SEEK_END)  # Move the file pointer to the end

        for album_index, album_url in enumerate(album_urls, 1):
            log.info(f'Album index: {album_index}')
            album_folder = os.path.join(destination_folder, f'album_{album_index}')
            os.makedirs(album_folder, exist_ok=True)
            driver = webdriver.Chrome(service=service, options=options)
            try:
                log.debug(f'running get_album_data for album_index: {album_index}')
                get_album_data(driver, album_url, album_folder, writer)
            except StaleElementReferenceException:
                log.error(f"Skipping album {album_index} due to stale element reference")

            driver.quit()
            f.flush()  # Flush the writer to update the file

def get_album_data(driver, album_url, album_folder, writer):
    driver.get(album_url)

    title_div = driver.find_element(By.CSS_SELECTOR, 'span.showalbumheader__gallerytitle')
    subtitle_div = driver.find_element(By.CSS_SELECTOR, 'div.showalbumheader__gallerysubtitle.htmlwrap__main')
    image_divs = driver.find_elements(By.CSS_SELECTOR, 'div.showalbum__children.image__main')

    title = title_div.text
    subtitle_content = subtitle_div.text

    match = re.search(r'(https?://\S+)', subtitle_content)
    link = match.group(1) if match else ''

    id = extract_unique_id(title)

    log.info(f"[ID: {id}] Album Title: {title}\tSubtitle Content: {subtitle_content}\tLink: {link}")

    images = []

    for i, image_div in enumerate(image_divs, 1):
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
    log.info(f"all images: {images}")

    # Prepare album data
    album_data = [id, title, subtitle_content, link, ','.join(images)]
    writer.writerow(album_data)

def extract_unique_id(string):
    pattern = r'AN\d+'  # Pattern for "AN" followed by one or more digits

    match = re.search(pattern, string)
    if match:
        unique_id = match.group()
        return unique_id
    else:
        return 'no ID'

# Example usage:
main_url = "https://taozi140.x.yupoo.com/albums"
destination_folder = "/Users/user/Desktop/yupoo"
log = logger_init()

options = Options()
options.add_argument('--headless')

chromedriver_path = '/path/to/chromedriver'
service = Service(chromedriver_path)

log.info(f"Opening main albums url: {main_url}")

driver = webdriver.Chrome(service=service, options=options)
driver.get(main_url)

album_links = driver.find_elements(By.CSS_SELECTOR, 'div.showindex__children a')
album_urls = [album_link.get_attribute('href') for album_link in album_links]
log.info(f"Quiting main albums url: {main_url}")

driver.quit()
log.info(f'Albums URLs Count: {len(album_urls)}')

download_images(album_urls, destination_folder)
