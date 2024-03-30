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

driver.get("https://genius.com/songs/all")

# Variable Declarations
song_url = ""
string_song_name = ""
string_lyrics = ""

primary_artists = []
song_names = []
link_element = []

# Function Definitions

def binary_search(existing_urls, url): 
    '''
    Uses BS to search for scraped songs in song_urls.txt
    '''
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

def cleanup_text(text):
    '''
    Cleans up text to be ready for insertion in DB (For cosine similarity)
    '''
    text_without_brackets = re.sub(r'\[[^\]]*\]', '', text)
    text_without_quotes = text_without_brackets.replace('"', '')
    cleaned_text = re.sub(r'\n\s*\n', '\n', text_without_quotes)
    return cleaned_text.strip()

def get_URLs():
    '''
    Gets song URLs from song_urls.txt
    '''
    with open('back-end/song_urls.txt', 'r') as file:
        existing_urls = file.readlines()                    # existing_urls is an array with all urls from .txt
    existing_urls = [url.strip() for url in existing_urls]  # Removes newline characters and whitespace
    return existing_urls


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


# --------------- Scrolls through the entirety of the webpage -----------------

# Get initial page height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scrolls down to the bottom of the page
    
    sleep(3)    # Waits for the webpage to load

    # Wait for new page height to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    
    # Check if the page height remains the same, indicating the end of the page
    if new_height == last_height:
        break
    
    last_height = new_height
    
    print(f"Scrolling... Currently at: {last_height}")
    
    # ----------- Gets Song Name, Artist, and URL from Genius.com (Selenium) --------------------

    new_primary_artists = driver.find_elements(By.CLASS_NAME, "primary_artist_name")
    new_song_names = driver.find_elements(By.CLASS_NAME, "title_with_artists")
    new_link_element = driver.find_elements(By.CLASS_NAME, "song_link")
    
    primary_artists = [elem for elem in new_primary_artists if elem not in primary_artists]         # Filters out already processed data
    song_names = [elem for elem in new_song_names if elem not in song_names]
    link_element = [elem for elem in new_link_element if elem not in link_element]
    
    existing_urls = get_URLs()              # puts all URLs from song_urls.txt into a list
    
    for i in range(len(song_names)):
        
        # ----------- Checks for duplicate song urls & inserts non-duplicates  --------------------
        song_url = link_element[i].get_attribute('href')
        insert_index, is_duplicate = binary_search(existing_urls, song_url)
        if (is_duplicate):
            print("Skipping Duplicate Entry")
            continue
        
        else:   
            # ----------- Gets the source code of the lyrics of a song (BS4) --------------------   
            index = 0
            lyricsDriver.get(song_url)
            
            string_lyrics = ""
            try:
                lyrics = WebDriverWait(lyricsDriver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1'))            # loads page until lyrics are found
                )
                print("Lyrics Container element has appeared!")
                
                lyrics = lyricsDriver.find_elements(By.CSS_SELECTOR, '.Lyrics__Container-sc-1ynbvzw-1.kUgSbL')            # finds the lyrics
                
                for lyric in lyrics:
                    string_lyrics += cleanup_text(lyric.text.lower())
                    
                index += 1

            except Exception as e:                                                                                  # if lyrics are not found
                print(f"An error occurred: {e}")
        
        
            # ------------------ Gets the song name --------------------   
            try:
                string_song_name = song_names[i].text.split(' – ')[1].strip()     # split splits the string upon seeing '-' into a dictionary with n elements
                string_song_name = string_song_name.replace('Lyrics', '')               # gets rid of the word "Lyrics"
                string_song_name = string_song_name[:-1]                                # gets rid of extra space at the end of the string

            except IndexError:
                print("Song name not found.")
                
            # ------------------ Gets the albumn image --------------------
            try:
                # Find the image element by its class names separately
                image_element = lyricsDriver.find_element(By.CLASS_NAME, "SizedImage__Image-sc-1hyeaua-1")

                # Get the source URL of the image
                image_source_url = image_element.get_attribute('src')

                # Download the image using the requests library
                if image_source_url:
                    image_content = requests.get(image_source_url).content
                    print('Albumn Image Found')
                    
                else:
                    print('Image source URL not found')

            except Exception as e:
                print(f"Error: {e}")
                driver.quit()    
                
                
            # --------------- Adds the data into MongoDB -------------------- 
            song = {
                "title": string_song_name,
                "artist": primary_artists[i].text,
                "lyrics": string_lyrics,    
                "lyrics_url": song_url,
                "albumn_image_data" : image_content
            }    
            
            collection.insert_one(song)            # Adds a song document to the collection
            
            # ------------------ Add URL to the existing list of links --------------------
            existing_urls.insert(insert_index, song_url)
            with open('back-end/song_urls.txt', 'w') as file:
                file.write('\n'.join(existing_urls))
            existing_urls = get_URLs()     
            
            print(f"Successfully inserted: {string_song_name} by {primary_artists[i].text}")
    
print("Done Scrolling!")
print("end")
driver.quit()
lyricsDriver.quit()