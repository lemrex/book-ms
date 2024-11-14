import logging
from pymongo import MongoClient
from dotenv import load_dotenv
import os


# Load environment variables from the .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Use environment variables for MongoDB connection string and database name
mongo_user = os.getenv('MONGO_USER')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_host = os.getenv('MONGO_HOST')  # or the appropriate hostname of your MongoDB service
database_name = os.getenv('MONGO_DB')

# Initialize MongoDB connection
mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:27017/{database_name}"

logger.info(f"Connecting to MongoDB URI: {mongo_uri}")
try:
    client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # Set a timeout for the connection
    # Test the connection to MongoDB
    client.server_info()  # This will raise an exception if the connection fails
    db = client[database_name]
    books_collection = db['books']
    logger.info("Successfully connected to MongoDB")
except Exception as e:
    logger.error(f"Error connecting to MongoDB: {e}")

def init_db(books_collection=None):
    if books_collection is not None:
        logger.error("books_collection is None. Database initialization skipped.")
        return
    try:
        # Create indexes if needed
        books_collection.create_index([('isbn', 1)], unique=True)
        books_collection.create_index([('user_id', 1)])
        logger.info("Database initialized with indexes")
    except Exception as e:
        logger.error(f"Error initializing database indexes: {e}")
    else:
        logger.error("books_collection is not available. Database initialization skipped.")



