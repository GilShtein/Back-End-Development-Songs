from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401
from pymongo import MongoClient
from bson import json_util
from pymongo.errors import OperationFailure
from pymongo.results import InsertOneResult
from bson.objectid import ObjectId
import sys

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))



# client = MongoClient(
#     f"mongodb://{app.config['MONGO_USERNAME']}:{app.config['MONGO_PASSWORD']}@localhost")
mongodb_service = "localhost" #os.environ.get('MONGODB_SERVICE')
mongodb_username = "" #os.environ.get('MONGODB_USERNAME')
mongodb_password = "" # os.environ.get('MONGODB_PASSWORD')
mongodb_port = "27017" #os.environ.get('MONGODB_PORT')

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service == None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    # abort(500, 'Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

if mongodb_username and mongodb_password:
    url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}"
else:
    url = f"mongodb://{mongodb_service}"


print(f"connecting to url: {url}")

try:
    client = MongoClient(url)
except OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

db = client.songs
db.songs.drop()
db.songs.insert_many(songs_list)

def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# INSERT CODE HERE
######################################################################
@app.route("/health", methods=["GET"])
def health():
    return jsonify(dict(status="OK")), 200


@app.route("/count")
def count():
    """return length of data"""
    if songs_list:
        return jsonify(length=len(songs_list)), 200

    return {"message": "Internal server error"}, 500

@app.route("/songs", methods=["GET"])
def get_songs():
    """Return all songs"""
    try:
        # Fetch all documents from the 'songs' collection
        songs_cursor = db.songs.find({})
        songs = list(songs_cursor)  # Convert cursor to list
        # Convert the list of documents to JSON serializable format
        songs = parse_json(songs)
        return jsonify({"songs": songs}), 200
    except Exception as e:
        app.logger.error(f"Error fetching songs: {str(e)}")
        return jsonify({"error": "Error fetching songs"}), 500




@app.route("/songs/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    songs_cursor = db.songs.find({})
    songs = list(songs_cursor)  # Convert cursor to list
    for item in songs:
        if item["id"] == id:
            return jsonify(parse_json(item)), 200
    return jsonify({"message": "No pictures found"}), 404




# Function to convert MongoDB documents to JSON-serializable format
def convert_object_id(document):
    document['_id'] = str(document['_id'])  # Convert ObjectId to string
    return document


@app.route("/songs", methods=["POST"])
def create_song():
    new_song = request.get_json()
    print(new_song)
    if not new_song:
        # Return a JSON response indicating that the request data is invalid or missing
        # with a status code of 400 (Bad Request)
        return {"message": "Invalid input, no data provided"}, 400
    songs_cursor = db.songs.find({})
    songs = list(songs_cursor)  # Convert cursor to list
    for item in songs:
        if item["id"] == new_song["id"]:
            return {"Message": f"song with id {new_song['id']} already present"}, 302
    db.songs.insert_one(new_song)
    return jsonify(convert_object_id(new_song)), 201

@app.route("/songs/<int:id>", methods=["PUT"])
def update_song(id):
    new_song = request.get_json()
    if not new_song:
        # Return a JSON response indicating that the request data is invalid or missing
        # with a status code of 400 (Bad Request)
        return {"message": "Invalid input, no data provided"}, 400
    song = db.songs.find_one({"id":id})
    if song:
        changes = {"$set" : new_song }
        db.songs.update_one({"id": id}, changes)
        return jsonify(new_song), 201

    return {"message": " song not found"}, 404


@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    res = db.songs.delete_one({"id":id})
    if res.deleted_count == 1:
        return jsonify(), 204

    return {"message": "song not found"}, 404
