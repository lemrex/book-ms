from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Use environment variables for MongoDB connection string and database name
mongo_uri = os.getenv('MONGO_URI')
database_name = os.getenv('MONGO_DB')

# Initialize MongoDB connection
client = MongoClient(mongo_uri)
db = client[database_name]
books_collection = db['books']

def init_db():
    # Create indexes if needed
    books_collection.create_index([('isbn', 1)], unique=True)
    books_collection.create_index([('user_id', 1)])
    print("Database initialized")
