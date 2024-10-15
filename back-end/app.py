import base64
from flask import Flask, request, jsonify
from flask import Flask
from thefuzz import fuzz
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi
import random

app = Flask(__name__)

CORS(app) # gives permissions to access data

# MongoDB set up

uri = "mongodb+srv://jesse1333:Justin0122_!@songdatacluster.jdvhjag.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["song_library_db"]
collection = db["songs"]
collection.create_index([("lyrics", "text")])

# function to search for similarity
@app.route('/search', methods=['POST'])
def search():
    data = request.json    
    search_query = data.get('query')
    
    # MongoDB text search
    search_results = collection.find(
        {"$text": {"$search": search_query}},
        {"score": {"$meta": "textScore"}}
    ).sort([("score", {"$meta": "textScore"})])

    search_results_list = list(search_results)

    # Function to calculate similarity scores using FuzzyWuzzy
    def calculate_similarity(query, document):
        return fuzz.partial_ratio(query, document['lyrics'])

    refined_results = []
    for result in search_results_list:
        similarity_score = calculate_similarity(search_query, result)

        if similarity_score >= 60:
            refined_results.append({
                "title": result['title'],
                "similarity_score": similarity_score,
                "lyrics_url": result.get('lyrics_url'),  # Include the lyrics URL
                "albumn_image_data": base64.b64encode(result.get('albumn_image_data')).decode('utf-8') if result.get('albumn_image_data') else None,  # Convert to Base64
            })
            
    refined_results.sort(key=lambda x: x['similarity_score'], reverse=True)
    
    return jsonify(refined_results)


@app.route('/random_songs', methods=['GET'])
def get_random_songs():
    collection = db["songs"] 

    # Count the total number of songs in the collection
    total_songs = collection.count_documents({})
    
    if total_songs == 0:
        return jsonify({"error": "No songs found in the database."}), 404

    # Determine how many songs to fetch (up to 3)
    num_songs_to_fetch = min(3, total_songs)

    # Get distinct random indices
    random_indices = random.sample(range(total_songs), num_songs_to_fetch)

    # Retrieve random songs
    random_songs = [collection.find().skip(index).limit(1)[0] for index in random_indices]

    # Format the response to include title, artist, lyrics, and album image data
    response = []
    for song in random_songs:
        # Convert binary image data to base64 string if it exists
        image_data = base64.b64encode(song['albumn_image_data']).decode('utf-8') if 'albumn_image_data' in song else None
        
        response.append({
            "title": song["title"],
            "artist": song["artist"],
            "lyrics": song["lyrics"],
            "lyrics_url": song.get("lyrics_url", ""),
            "similarity_score": song.get("similarity_score", None),  # Include if exists
            "albumn_image_data": image_data  # Pass the base64 image data
        })
    
    return jsonify(response)


# @app.route('/random_songs', methods=['GET'])
# def get_random_songs():
#     # Count the total number of songs in the collection
#     total_songs = collection.count_documents({})
    
#     if total_songs == 0:
#         return jsonify({"error": "No songs found in the database."}), 404

#     # Determine how many songs to fetch (up to 3)
#     num_songs_to_fetch = min(3, total_songs)

#     # Get distinct random indices
#     random_indices = random.sample(range(total_songs), num_songs_to_fetch)

#     # Retrieve random songs
#     random_songs = [collection.find().skip(index).limit(1)[0] for index in random_indices]

#     # Format the response
#     response = [{
#         "title": song["title"],
#         "lyrics": song["lyrics"]
#     } for song in random_songs]
    
#     return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)