# import logging
# from pymongo import MongoClient
# from dotenv import load_dotenv
# import os


# # Load environment variables from the .env file
# load_dotenv()

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# # Use environment variables for MongoDB connection string and database name
# # mongo_uri = os.getenv('MONGO_URI')
# # database_name = os.getenv('MONGO_DB')
# mongo_user = os.getenv('MONGO_USER')
# mongo_password = os.getenv('MONGO_PASSWORD')
# mongo_host = os.getenv('MONGO_HOST')  # or the appropriate hostname of your MongoDB service
# database_name = os.getenv('MONGO_DB')

# # Initialize MongoDB connection
# mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@{mongo_host}:27017/{database_name}"

# logger.info(f"Connecting to MongoDB URI: {mongo_uri}")
# try:
#     client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)  # Set a timeout for the connection
#     # Test the connection to MongoDB
#     client.server_info()  # This will raise an exception if the connection fails
#     db = client[database_name]
#     books_collection = db['books']
#     logger.info("Successfully connected to MongoDB")
# except Exception as e:
#     logger.error(f"Error connecting to MongoDB: {e}")

# def init_db():
#     # Check if we have successfully connected before initializing the DB
#     if 'books_collection' in locals():
#         # Create indexes if needed
#         books_collection.create_index([('isbn', 1)], unique=True)
#         books_collection.create_index([('user_id', 1)])
#         logger.info("Database initialized with indexes")
#     else:
#         logger.error("Failed to connect to MongoDB. Database initialization skipped.")


import logging
from typing import Optional
from pymongo import MongoClient, ASCENDING
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError, OperationFailure
from dotenv import load_dotenv
import os
from contextlib import contextmanager

class MongoDBHandler:
    """
    A handler class for MongoDB connections and operations with proper error handling
    and connection management.
    """
    
    def __init__(self):
        # Set up logging
        self.logger = logging.getLogger(__name__)
        
        # Load environment variables
        load_dotenv()
        
        # Initialize connection attributes
        self.client: Optional[MongoClient] = None
        self.db: Optional[Database] = None
        self.books_collection: Optional[Collection] = None
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load and validate MongoDB configuration from environment variables."""
        required_vars = ['MONGO_USER', 'MONGO_PASSWORD', 'MONGO_HOST', 'MONGO_DB']
        config = {}
        
        for var in required_vars:
            value = os.getenv(var)
            if not value:
                raise ValueError(f"Missing required environment variable: {var}")
            config[var] = value
            
        return config
    
    def get_connection_uri(self) -> str:
        """Construct MongoDB connection URI from configuration."""
        return (f"mongodb://{self.config['MONGO_USER']}:{self.config['MONGO_PASSWORD']}"
                f"@{self.config['MONGO_HOST']}:27017/{self.config['MONGO_DB']}")
    
    def connect(self) -> None:
        """Establish connection to MongoDB and initialize collections."""
        if self.client is not None:
            self.logger.warning("Connection already exists")
            return
            
        try:
            uri = self.get_connection_uri()
            self.logger.info("Attempting to connect to MongoDB...")
            
            # Create client with timeout and retry options
            self.client = MongoClient(
                uri,
                serverSelectionTimeoutMS=5000,
                retryWrites=True,
                connectTimeoutMS=5000
            )
            
            # Test connection
            self.client.server_info()
            
            # Initialize database and collections
            self.db = self.client[self.config['MONGO_DB']]
            self.books_collection = self.db['books']
            
            self.logger.info("Successfully connected to MongoDB")
            
            # Initialize database indexes
            self._init_indexes()
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error during MongoDB connection: {e}")
            raise
    
    def _init_indexes(self) -> None:
        """Initialize required indexes for collections."""
        try:
            # Create indexes with proper options
            self.books_collection.create_index(
                [('isbn', ASCENDING)],
                unique=True,
                background=True
            )
            self.books_collection.create_index(
                [('user_id', ASCENDING)],
                background=True
            )
            self.logger.info("Database indexes initialized successfully")
            
        except OperationFailure as e:
            self.logger.error(f"Failed to create indexes: {e}")
            raise
    
    def disconnect(self) -> None:
        """Close MongoDB connection safely."""
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.books_collection = None
            self.logger.info("Disconnected from MongoDB")
    
    @contextmanager
    def get_connection(self):
        """Context manager for handling MongoDB connections."""
        try:
            if not self.client:
                self.connect()
            yield self
        finally:
            self.disconnect()
    
    def is_connected(self) -> bool:
        """Check if the connection to MongoDB is active."""
        if not self.client:
            return False
        try:
            self.client.server_info()
            return True
        except ServerSelectionTimeoutError:
            return False

# Usage example:
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create handler instance
    mongo_handler = MongoDBHandler()
    
    # Use the context manager for automatic connection handling
    with mongo_handler.get_connection() as mongo:
        if mongo.is_connected():
            print("Successfully connected to MongoDB")



