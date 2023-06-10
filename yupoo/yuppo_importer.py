import os
import csv
import requests
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def download_images(album_url, destination_folder):
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Configure Selenium options
    options = Options()
    options.add_argument('--headless')  # Run Chrome in headless mode

    # Set the path to your ChromeDriver executable
    chromedriver_path = '/path/to/chromedriver'

    # Set up the Selenium service
    service = Service(chromedriver_path)

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Navigate to the album URL
    driver.get(album_url)

    image_urls = []

    # Find the div tag with class "showalbumheader__gallerytitle"
    title_div = driver.find_element(By.CSS_SELECTOR, 'span.showalbumheader__gallerytitle')

    # Extract the title from the div element
    title = title_div.text

    # Print the title
    print("Album Title:")
    print(title)
    print()

    # Find the div tag with class "showalbumheader__gallerysubtitle htmlwrap__main"
    subtitle_div = driver.find_element(By.CSS_SELECTOR, 'div.showalbumheader__gallerysubtitle.htmlwrap__main')

    # Print the content of the div element
    subtitle_content = subtitle_div.text
    print("Subtitle Content:")
    print(subtitle_content)
    print()

    # Find all div tags with class "showalbum__children.image__main"
    image_divs = driver.find_elements(By.CSS_SELECTOR, 'div.showalbum__children.image__main')

    for i, image_div in enumerate(image_divs, 1):
        # Find the img tag within the div
        img_tag = image_div.find_element(By.CSS_SELECTOR, 'img')

        # Extract the image URL from the data-src attribute of the img tag
        image_url = img_tag.get_attribute('src')

        # Check if the image URL contains the scheme
        parsed_url = urljoin(album_url, image_url)

        # Modify headers to include User-Agent and Referer
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36',
            'Referer': album_url
        }

        image_name = f"image_{i}.png"

        # Download the image and save it in the destination folder
        response = requests.get(parsed_url, headers=headers)
        response.raise_for_status()

        with open(os.path.join(destination_folder, image_name), 'wb') as f:
            f.write(response.content)

        image_urls.append(parsed_url)


        print(f"Downloaded image: {image_name}")

    # Quit the browser
    driver.quit()

    create_csv(destination_folder, image_urls, subtitle_content, title)


def create_csv(destination_folder, image_urls, subtitle_content, title):
    # Create the CSV file and write the album information
    csv_path = os.path.join(destination_folder, 'album_info.csv')
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['title', 'content', 'images'])
        writer.writerow([title, subtitle_content, ', '.join(image_urls)])
    print(f"Album information saved to: {csv_path}")


# Example usage:
album_url = "https://taozi140.x.yupoo.com/albums/134749293?uid=1&utm_source=copyLink"  # Replace with the actual album URL

# album_url = 'https://8618588998232.x.yupoo.com/albums/135792857?uid=1&isSubCate=false&referrercate=3499562'

destination_folder = "/Users/user/Desktop/yupoo"  # Replace with the desired destination folder

# Download images related to the album
download_images(album_url, destination_folder)

# Copy the album description
# copy_album_description(album_url)
