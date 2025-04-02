from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient
from flask_cors import CORS  # To allow cross-origin requests from React frontend

from bson import ObjectId
import gridfs
import io

app = Flask(__name__)
CORS(app)

# Connect to MongoDB Atlas
atlas_connection_string = "mongodb+srv://db_admin:dQERttM5UIXM41cy@cluster0.ofqfm.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(atlas_connection_string)

# Specify your database and collection
db = client['woodridgekiosk']  # Database name
collection = db['businesses']  # Collection 
fs = gridfs.GridFS(db)

@app.route('/api/businesses', methods=['GET'])
def get_businesses():
    businesses = list(collection.find()) # Get all businesses
    # print(businesses)
    for business in businesses:
        business['_id'] = str(business['_id'])  # Convert ObjectId to string
        business['image'] = str(business['image'])  # Convert ObjectId to string
    
    return jsonify(businesses)

@app.route('/image/<file_id>', methods=['GET'])
def get_image(file_id):
    # Fetch the file by its ObjectId
    file = fs.get(ObjectId(file_id))
    return send_file(io.BytesIO(file.read()), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)