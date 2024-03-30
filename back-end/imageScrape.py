import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException  
from selenium.webdriver.chrome.service import Service
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from time import sleep


# --------------- Selenium Set-up -----------------
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-gpu')

driver = webdriver.Chrome(options=chrome_options)
lyricsDriver = webdriver.Chrome(options=chrome_options)

driver.get("https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics")

try:
    # Find the image element by its class names separately
    image_element = driver.find_element(By.CLASS_NAME, "SizedImage__Image-sc-1hyeaua-1")

    # Get the source URL of the image
    image_source_url = image_element.get_attribute('src')

    # Close the WebDriver
    driver.quit()

    # Download the image using the requests library
    if image_source_url:
        image = requests.get(image_source_url)
        with open('image.jpg', 'wb') as file:
            file.write(image.content)
            print('Image downloaded successfully')
    else:
        print('Image source URL not found')

except Exception as e:
    print(f"Error: {e}")
    driver.quit()