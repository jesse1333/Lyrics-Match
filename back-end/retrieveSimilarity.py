from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from thefuzz import fuzz
from thefuzz import process

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

collection.create_index([("lyrics", "text")])   # Creates a text index for "lyrics"


search_query = "and if you think im hold you should love yourself"  # Example search term

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

# Print refined results
for entry, score in refined_results:
    print(f"Document: {entry['title']}, Similarity Score: {score}")