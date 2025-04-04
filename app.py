# required libraries 
from flask import Flask, jsonify, send_file # Flask is a lightweight, open-source Python microframework for building web applications
from pymongo import MongoClient # PyMongo is the official MongoDB driver for Python, a library that enables Python applications to connect to and interact with MongoDB databases
from flask_cors import CORS  # To allow cross-origin requests from React frontend

from bson import ObjectId # BSON, the binary representation of JSON, is primarily used internally by MongoDB for efficient storage and data traversal.
from bson.errors import InvalidId # Error if item ID is wrong
import gridfs # GridFS is a file storage system in MongoDB
import io # Python io module allows us to manage the file-related input and output operations

# Create an instance of flask web application framework
app = Flask(__name__)
# enables cross-origin request
CORS(app)

# Connect to MongoDB Atlas
atlas_connection_string = "mongodb+srv://db_admin:XEnMjPDPcFWIbh8Q@cluster0.ofqfm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(atlas_connection_string)

# Specify your database and collection
db = client['woodridgekiosk']  # Database name
collection = db['businesses']  # Collection 
fs = gridfs.GridFS(db) # split data into chunks or into a bucket

# Get all businesses data
@app.route('/api/businesses', methods=['GET'])
def get_businesses() -> list:
    businesses = list(collection.find()) # Get all businesses
    # print(businesses)
    for business in businesses:
        business['_id'] = str(business['_id'])  # Convert ObjectId to string
        business['image'] = str(business['image'])  # Convert ObjectId to string
    
    return jsonify(businesses) # convert data into json format

# Get specific business data based on business ID
@app.route('/api/business/<business_id>', methods=['GET'])
def get_business(business_id) -> list:
    try:
        # .find_one - search data in mongodb based on _id
        business = collection.find_one({"_id": ObjectId(business_id)})
        if business:
            business['_id'] = str(business['_id']) # Convert ObjectId to string
            business['image'] = str(business['image']) # Convert ObjectId to string
            return jsonify(business)
        else:
            return jsonify({ 'error': 'Business not found' }), 404
    except InvalidId:
        return jsonify({"error": "Invalid business ID format"}), 400

# Get image
@app.route('/api/image/<file_id>', methods=['GET'])
def get_image(file_id):
    # Fetch the file by its ObjectId
    file = fs.get(ObjectId(file_id))
    return send_file(io.BytesIO(file.read()), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)