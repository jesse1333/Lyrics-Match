from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

driver = webdriver.Chrome()

driver.get("https://genius.com/Luis-fonsi-and-daddy-yankee-despacito-remix-lyrics")


# ----------- Gets the source code of the lyrics of a song (BS4) --------------------

# lyrics = driver.find_element(By.CLASS_NAME, 'Lyrics__Container-sc-1ynbvzw-1 kUgSbL')


# print(lyrics)



try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1'))
    )
    print("Element has appeared!")
    
    lyrics = driver.find_elements(By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')
    
    for lyric in lyrics:
        print(lyric.text)
    
    # You can now proceed with further actions involving this element
except Exception as e:
    print(f"An error occurred: {e}")
    
    
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CSS_SELECTOR, '.ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw'))
#     )
#     print("Element has appeared!")
    
#     lyrics = driver.find_elements(By.CSS_SELECTOR, '.ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw')
#     for lyric in lyrics:
#         print(lyric.text)
    
#     # You can now proceed with further actions involving this element
# except Exception as e:
#     print(f"An error occurred: {e}")


# # ----------- Rids of non-lyrics from source code (ie tags <>)  --------------------
# isCopying = True
# stringLyrics = ""                       # Lyrics will end up not completely formatted (can't differentiate new lines for lyrics)

# for lyric in str(lyrics):
#     if lyric == '<':
#         isCopying = False
        
#     if isCopying:
#         stringLyrics += str(lyric)
        
#     if lyric == '>':
#         isCopying = True
        
# print(stringLyrics)



driver.quit()

print("END")






















# # ----------- Gets the source code of the lyrics of a song (BS4) --------------------
# result = requests.get("https://genius.com/Eminem-rap-god-lyrics")                                                       # sends an HTML request to the website and gets the code           
# soupLyrics = BeautifulSoup(result.text, "html.parser")                                  # parses html code into variable
# lyrics = soupLyrics.find('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')         # finds lyrics within code


# # ----------- Rids of non-lyrics from source code (ie tags <>)  --------------------
# isCopying = True
# stringLyrics = ""                       # Lyrics will end up not completely formatted (can't differentiate new lines for lyrics)

# for lyric in str(lyrics):
#     if lyric == '<':
#         isCopying = False
        
#     if isCopying:
#         stringLyrics += str(lyric)
        
#     if lyric == '>':
#         isCopying = True
        
# print(stringLyrics)


# driver.quit()

# print("END")