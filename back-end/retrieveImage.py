from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

import pymongo
from thefuzz import fuzz
from thefuzz import process
import json

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


def find_element_by_id(element_id):
    try:
        query = {"_id": ObjectId(element_id)}
        cursor = collection.find(query)

        for document in cursor:
            print(document)
    except Exception as e:
        print("Error:", e)

# Usage: Call the function with the ID of the element you want to retrieve
element_id = "6575e9eb4ab41c12aafa098d"  # Replace with the ID of the element
find_element_by_id(element_id)