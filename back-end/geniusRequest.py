from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from time import sleep


# --------------- Selenium Set-up -----------------
driver = webdriver.Chrome()
lyricsDriver = webdriver.Chrome()

driver.get("https://genius.com/songs/all")

# Variable Declarations
song_url = ""
string_song_name = ""
string_lyrics = ""


# --------------- MongoDB Set-up -----------------

uri = "mongodb+srv://jesse1333:Justin0122_!@songdatacluster.jdvhjag.mongodb.net/?retryWrites=true&w=majority" # Uniform Resource Identifier 
                                                                                                              # In the case of MongoDB, it has the info 
                                                                                                              # needed to locate and connect to the database

# Create a new client and connect to the server (Client is just a computer that requests access to the server)
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
    
db = client["song_library_db"]         # Gets the database (song_library_db)
collection = db["songs"]               # Gets the collection (songs)
    
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
    
    # ----------- Checks for duplicate song urls & inserts non-duplicates  --------------------
    song_url = link_element[i].get_attribute('href')
    insert_index, is_duplicate = binary_search(existing_urls, song_url)
    if (is_duplicate):
        continue
    
    else:
        # ------------------ Add URL to the existing list of links --------------------
        existing_urls.insert(insert_index, song_url)
        with open('back-end/song_urls.txt', 'w') as file:
            file.write('\n'.join(existing_urls))
        existing_urls = get_URLs()        
        
        # ----------- Gets the source code of the lyrics of a song (BS4) --------------------   
        index = 0
        lyricsDriver.get(song_url)
        
        # note: song_url works
        # note: there are 49 songs (i)
        
        string_lyrics = ""
        try:
            lyrics = WebDriverWait(lyricsDriver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1'))            # loads page until lyrics are found
            )
            print("Lyrics Container element has appeared!")
            
            lyrics = lyricsDriver.find_elements(By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')            # finds the lyrics
            
            for lyric in lyrics:
                string_lyrics += lyric.text
                string_lyrics += "\n"
                
            index += 1

        except Exception as e:                                                                                  # if lyrics are not found
            print(f"An error occurred: {e}")
    
    
        # ------------------ Gets the song name --------------------   
        try:
            string_song_name = song_names[i].text.split(' – ')[1].strip()           # split splits the string upon seeing '-' into a dictionary with n elements
            string_song_name = string_song_name.replace('Lyrics', '')               # gets rid of the word "Lyrics"
            string_song_name = string_song_name[:-1]                                # gets rid of extra space at the end of the string

        except IndexError:
            print("Song name not found.")
            
            
        # --------------- Adds the data into MongoDB -------------------- 
        song = {
            "title": string_song_name,
            "artist": primary_artists[i].text,
            "lyrics": string_lyrics,    
        }    
        
        collection.insert_one(song)            # Adds a song document to the collection


print("end")
driver.quit()
lyricsDriver.quit()
