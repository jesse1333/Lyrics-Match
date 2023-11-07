from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# Initialize the WebDriver
driver = webdriver.Chrome()

# Navigate to the URL of the web page you want to inspect
url = 'https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics'
driver.get(url)

# Retrieve the HTML code of the page
page_source = driver.page_source

# Print or save the HTML code as needed
# print(page_source)


time.sleep(10)

# inspect elements have different XPATH values for differnt pages. I need to figure out how to get the "correct" one
# All lyrics are found within Lyrics__Container-sc-1ynbvzw-1 kUgSbL though

lyrics = driver.find_elements(By.CLASS_NAME, "Lyrics__Container-sc-1ynbvzw-1 kUgSbL")



# lyrics = driver.find_elements_by_class_name("Lyrics__Container-sc-1ynbvzw-1 kUgSbL")

# for lyric in lyrics:
#     lyric = lyrics.find_element_by_xpath('.//*[@id="lyrics-root"]/div[3]')
    
print(lyrics)


# Close the browser
driver.quit()