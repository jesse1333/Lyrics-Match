import json
import base64
from flask import Flask, jsonify, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from thefuzz import fuzz

app = Flask(__name__)

uri = "mongodb+srv://jesse1333:Justin0122_!@songdatacluster.jdvhjag.mongodb.net/?retryWrites=true&w=majority"   # Uniform Resource Identifier 
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


# @app.route('/', methods=['POST'])    # this defines what happens the root URL is accessed (root url is when there are no additional paths like /about or something)
# def receieve_lyrics():
#     '''
#     This method retrieves the text from the frontend
#     '''
#     received_data = request.json
#     user_lyrics = received_data.get('userLyrics')  # Access 'textData' sent from frontend

#     # Process 'textData' received from frontend
#     print('Received text data:', user_lyrics)

#     # Return a response to the frontend
#     return jsonify({"message": "Text data received successfully"})


@app.route('/', methods=['POST'])    # this defines what happens the root URL is accessed (root url is when there are no additional paths like /about or something)
def process_lyrics():
    '''
    This method retrieves the text from the frontend, processes it and returns it to the frontend
    '''
    received_data = request.json
    user_lyrics = received_data.get('userLyrics')  # Access 'textData' sent from frontend

    # Process 'textData' received from frontend
    print('Received text data:', user_lyrics)
    
    # Return a response to the frontend    
    return jsonify(get_similar_songs(user_lyrics))


def get_similar_songs(user_lyrics):
    '''
    This method returns the top 3 most similar songs from the database (in dictionary form)
    '''

    db = client["song_library_db"]         # Gets the database (song_library_db)
    collection = db["songs"]               # Gets the collection (songs)

    collection.create_index([("lyrics", "text")])   # Creates a text index for "lyrics"

    if user_lyrics != "":
        search_query = user_lyrics                      # Lyrics to search for
    else:
        return

    # MongoDB text search to get initial results
    search_results = collection.find(
        {"$text": {"$search": search_query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])

    # Convert search_results to a list
    search_results_list = list(search_results)

    # Function to calculate similarity scores using FuzzyWuzzy (it will get the field in lyrics)
    def calculate_similarity(query, document):
        return fuzz.partial_ratio(query, document['lyrics'])

    refined_results = []
    for result in search_results_list:
        similarity_score = calculate_similarity(search_query, result)
        
        # If the lyrics are past 60% similarity, we add the result to the list
        if similarity_score >= 60:
            refined_results.append((result, similarity_score))

    # Sorts songs into descending order
    sorted_results = sorted(refined_results, key=lambda x: x[1], reverse=True)
    
    top_3_results = sorted_results[:3]
    
    top_3_entries_dict = {
        f"Song {i + 1}": {"title": entry['title'], "artist" : entry['artist'], "lyrics" : entry['lyrics'], "lyrics_url" : entry['lyrics_url'], "albumn_image_data" : base64.b64encode(entry['albumn_image_data']).decode('utf-8'), "similarity_score": score}
        for i, (entry, score) in enumerate(top_3_results)
    }
    
    # Keys are "Song 1", "Song 2" and "Song 3"
    # To access specific data (dictionary in the dictionary) top_3_entries_dict["Song 1"]["lyrics"]

    return top_3_entries_dict

if __name__ == '__main__':
    app.run(debug=True)