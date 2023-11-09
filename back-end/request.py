from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

url = "https://genius.com/songs/all"

result = requests.get(url)      # sends an HTML request to the website and gets the code           

soupMain = BeautifulSoup(result.text, "html.parser")    # result.text holds the parsed HTML document, and html.parser tells the program to parse with HTML parser

print(soupMain.prettify())          # just helps visualize the HTML code




# ----------- Gets Song Information from main page --------------------

song_name_element = soupMain.find('a', class_='song_name')              # finds the <a> tag that has class 'song_name' 
                                                                        # Note: classes in <a> are seperated by space (so has multiple classes)

if song_name_element:
    song_name = song_name_element['title'].split(' – ')[1]              # split splits the string upon seeing '-' into a dictionary with n elements
    song_name = song_name.replace('Lyrics', '')
    artist = song_name_element['title'].split(' – ')[0]
    
    print("Song name: ", song_name)
    print("Artist: ", artist)
    
else:
    print("Song name not found.")


# ----------- Gets URL for the lyrics of a song --------------------

link_element = soupMain.find('a', class_='song_link')   

if link_element:
    lyrics_url = link_element.get('href')                           # gets the value of the 'href' element 
    print(lyrics_url) 
else:
    print("No matching elemnt found.")


# ----------- Gets the source code of the lyrics of a song --------------------

result = requests.get(lyrics_url)                                                       # sends an HTML request to the website and gets the code           
soupLyrics = BeautifulSoup(result.text, "html.parser")                                  # parses html code into variable
lyrics = soupLyrics.find('div', class_='Lyrics__Container-sc-1ynbvzw-1 kUgSbL')         # finds lyrics within code

print("PRINTING!")
print(lyrics.prettify()) 


# ----------- Rids of non-lyrics from source code (ie tags <>)  --------------------
isCopying = True
stringLyrics = ""                       # Lyrics will end up not completely formatted (can't differentiate new lines for lyrics)

for lyric in str(lyrics):
    if lyric == '<':
        isCopying = False
        
    if isCopying:
        stringLyrics += str(lyric)
        
    if lyric == '>':
        isCopying = True
        
print(stringLyrics)

song_name_element = soupMain.find_next('a', class_='song_name')              # finds the <a> tag that has class 'song_name' 

print(song_name_element.text())
