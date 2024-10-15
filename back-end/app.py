from flask import Flask, request, jsonify
from flask import Flask
from thefuzz import fuzz
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.server_api import ServerApi

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
                "similarity_score": similarity_score
            })
            
    return jsonify(refined_results)

if __name__ == '__main__':
    app.run(debug=True)



# from flask import Flask, request, jsonify
# from pymongo import MongoClient
# from pymongo.server_api import ServerApi
# from thefuzz import fuzz

# app = Flask(__name__)

# uri = "mongodb+srv://jesse1333:Justin0122_!@songdatacluster.jdvhjag.mongodb.net/?retryWrites=true&w=majority"
# client = MongoClient(uri, server_api=ServerApi('1'))
# db = client["song_library_db"]
# collection = db["songs"]

# # Create a text index for "lyrics"
# collection.create_index([("lyrics", "text")])

# @app.route('/search', methods=['POST'])
# def search():
#     data = request.get_json()
#     search_query = data.get('query', '')

#     # MongoDB text search to get initial results
#     search_results = collection.find(
#         {"$text": {"$search": search_query}},
#         {"score": {"$meta": "textScore"}}
#     ).sort([("score", {"$meta": "textScore"})])

#     # Convert search_results to a list
#     search_results_list = list(search_results)

#     # Function to calculate similarity scores using FuzzyWuzzy
#     def calculate_similarity(query, document):
#         return fuzz.partial_ratio(query, document['lyrics'])

#     refined_results = []
#     for result in search_results_list:
#         similarity_score = calculate_similarity(search_query, result)

#         # If the lyrics are past 60% similarity, we add the result to the list
#         if similarity_score >= 60:
#             refined_results.append({'title': result['title'], 'similarity_score': similarity_score})

#     return jsonify(refined_results)

# if __name__ == '__main__':
#     app.run(debug=True)
