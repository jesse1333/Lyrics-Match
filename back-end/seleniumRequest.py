from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://genius.com/songs/all")


# ----------- Gets Song Information from main page (Selenium) --------------------
primary_artists = driver.find_elements(By.CLASS_NAME, "primary_artist_name")
song_names = driver.find_elements(By.CLASS_NAME, "title_with_artists")
link_element = driver.find_elements(By.CLASS_NAME, "song_link")

primary_artist_list = []
song_name_list = []
song_url_list = []
song_lyrics_list = []
stringLyrics = ""

for i in range(len(primary_artists)):
    primary_artist_list.append(primary_artists[i].text)
    song_name_list.append(song_names[i].text)
    song_url_list.append(link_element[i].get_attribute('href'))
    
    try:
        song_name_list[i] = song_name_list[i].split(' – ')[1].strip()           # split splits the string upon seeing '-' into a dictionary with n elements
        song_name_list[i] = song_name_list[i].replace('Lyrics', '')

    except IndexError:
        print("Song name not found.")

# ----------- Gets the source code of the lyrics of a song (BS4) --------------------
print("HELO")




# for url in song_url_list:
#     result = requests.get(url)                                                              # sends an HTML request to the website and gets the code           
#     soupLyrics = BeautifulSoup(result.text, "html.parser")                                  # parses html code into variable
#     lyrics = soupLyrics.find(class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')                # finds lyrics within code

#     print("LYRICS: " + lyrics.text)
#     print()
#     print()
#     print()
#     # ----------- Rids of non-lyrics from source code (ie tags <>)  --------------------
#     isCopying = True

#     for lyric in lyrics.text:
#         if lyric == '<':
#             isCopying = False
            
#         if isCopying:
#             stringLyrics += str(lyric)                                     
            
#         if lyric == '>':
#             isCopying = True
    
#     song_lyrics_list.append(stringLyrics)
#     stringLyrics = ""

index = 0
for url in song_url_list:
    driver.get(url)
    
    try:
        lyrics = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1'))            # loads page until lyrics are found
        )
        print("Element has appeared!")
        
        lyrics = driver.find_elements(By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')            # finds the lyrics
        
        for lyric in lyrics:
            stringLyrics += lyric.text
            stringLyrics += "\n"
            
        song_lyrics_list.append(stringLyrics)
        
        print(song_lyrics_list[index])
        index += 1
    
    except Exception as e:                                                                                  # if lyrics are not found
        print(f"An error occurred: {e}")
    
    
    
    
    
    
    
    




# for elements in primary_artist_list:
#     print(f"Arist:{elements}")

# for elements in song_name_list:
#     print(f"Song name: {elements}")
    
# for elements in song_url_list:
#     print(f"Song URL: {elements}")

for elements in song_lyrics_list:
    print(f"Song Lyrics: {elements}")







print("end")



driver.quit()