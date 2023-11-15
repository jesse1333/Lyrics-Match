from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

driver.get("https://genius.com/songs/all")

# Variable Declarations

primary_artist_list = []
song_name_list = []
song_url_list = []
song_lyrics_list = []
stringLyrics = ""

# ----------- Gets Song Name, Artist, and URL from Genius.com (Selenium) --------------------

primary_artists = driver.find_elements(By.CLASS_NAME, "primary_artist_name")
song_names = driver.find_elements(By.CLASS_NAME, "title_with_artists")
link_element = driver.find_elements(By.CLASS_NAME, "song_link")

def binary_search(existing_urls, url):
    if not existing_urls:                 # case of an empty list
        return -1, False
    
    else:
        left = 0
        right = len(existing_urls) - 1
        is_duplicate = False

        while left <= right:
            mid = (left + right) // 2

            if existing_urls[mid] == url:
                is_duplicate = True
                return mid, is_duplicate  # Return the index and the duplicate flag
            elif existing_urls[mid] < url:
                left = mid + 1
            else:
                right = mid - 1

        return left, is_duplicate

def get_URLs():
    with open('back-end/song_urls.txt', 'r') as file:
        existing_urls = file.readlines()                    # existing_urls is an array with all urls from .txt
    existing_urls = [url.strip() for url in existing_urls]  # Removes newline characters and whitespace
    return existing_urls

existing_urls = get_URLs()              # puts all URLs from song_urls.txt into a list

for i in range(len(primary_artists)):
    # check the song_url
    insert_index, is_duplicate = binary_search(existing_urls, link_element[i].get_attribute('href'))
    if (is_duplicate):
        continue
    
    else:
        existing_urls.insert(insert_index, link_element[i].get_attribute('href'))
        with open('back-end/song_urls.txt', 'w') as file:
            file.write('\n'.join(existing_urls))
        existing_urls = get_URLs()        
    
        # # if not a duplicate, replace the rest of the code with adding directly to mongoDB
        # primary_artist_list.append(primary_artists[i].text)
        # song_name_list.append(song_names[i].text)
        # song_url_list.append(link_element[i].get_attribute('href'))
        
        
        # try:
        #     song_name_list[i] = song_name_list[i].split(' – ')[1].strip()           # split splits the string upon seeing '-' into a dictionary with n elements
        #     song_name_list[i] = song_name_list[i].replace('Lyrics', '')

        # except IndexError:
        #     print("Song name not found.")


# ----------- Checks for duplicate song urls & inserts non-duplicates  --------------------

# run a binary search to find song_urls in 'song_urls.txt' (returns true or false)






# def add_songs_to_file(song_urls):
#     # Read existing song URLs from the text file
#     with open('C:\\Users\\owner\\Documents\\GitHub\\Lyrics-Match\\back-end\\song_urls.txt', 'r') as file:
#         existing_urls = file.readlines()
#     existing_urls = [url.strip() for url in existing_urls]  # Removes newline characters and whitespace

#     # Add non-duplicate song URLs from the array to the list using binary search
#     for url in song_urls:
#         url = url.strip()  
#         insertion_index = binary_search(existing_urls, url)
#         if insertion_index == len(existing_urls) or existing_urls[insertion_index] != url:
#             existing_urls.insert(insertion_index, url)

#     # Sort the list of URLs alphabetically
#     existing_urls.sort()

#     # Write the updated list back to the text file
#     with open('C:\\Users\\owner\\Documents\\GitHub\\Lyrics-Match\\back-end\\song_urls.txt', 'w') as file:
#         file.write('\n'.join(existing_urls))
        




# # ----------- Gets the source code of the lyrics of a song (BS4) --------------------               # DONT DO THIS IF DUPLICATE LINK
# index = 0
# for url in song_url_list:
#     driver.get(url)
    
#     try:
#         lyrics = WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1'))            # loads page until lyrics are found
#         )
#         print("Element has appeared!")
        
#         lyrics = driver.find_elements(By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')            # finds the lyrics
        
#         for lyric in lyrics:
#             stringLyrics += lyric.text
#             stringLyrics += "\n"
            
#         song_lyrics_list.append(stringLyrics)
        
#         print(song_lyrics_list[index])
#         index += 1
    
#     except Exception as e:                                                                                  # if lyrics are not found
#         print(f"An error occurred: {e}")
    
    
print("end")
driver.quit()

