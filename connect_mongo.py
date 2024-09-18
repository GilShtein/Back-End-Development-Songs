from pymongo import MongoClient

# Create a MongoDB client and connect to the local MongoDB instance
client = MongoClient('localhost', 27017)

# Connect to a database
db = client['my_database']  # Replace 'my_database' with your database name

# Connect to a collection
collection = db['my_collection']  # Replace 'my_collection' with your collection name

# Insert a document into the collection
collection.insert_one({'name': 'John Doe', 'age': 29, 'city': 'New York'})

# Fetch a document from the collection
document = collection.find_one({'name': 'John Doe'})
print(document)
