from flask import Blueprint, request, jsonify
from bson import ObjectId
from src.models.book import Book
from src.config.redis import get_redis_client
import requests
import json
import logging
import os
from dotenv import load_dotenv

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

books_bp = Blueprint('books', __name__)
redis_client = get_redis_client()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def verify_token(token):
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    logger.info(f"Verifying token: {token}")
    
    # Use the URL from the environment variable
    verification_url = os.getenv('TOKEN_VERIFICATION_URL')
    try:
        response = requests.post(verification_url, json={'token': token})
        response.raise_for_status()  # Raises an exception for 4XX/5XX responses
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Token verification failed: {str(e)}")
        return {'valid': False, 'error': str(e)}

@books_bp.route('', methods=['GET'])
def get_books():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401

    verification = verify_token(token)
    if not verification['valid']:
        return jsonify({'error': 'Invalid token'}), 401

    user_id = verification['userId']

    # Try to get books from cache
    cached_books = redis_client.get(f'books:{user_id}')
    if cached_books:
        return jsonify(json.loads(cached_books))
    
    # If not in cache, get from database
    books = list(Book.find_by_user(user_id))
    
    # Convert ObjectId to string
    for book in books:
        book['_id'] = str(book['_id'])

    # Cache the result as JSON
    redis_client.setex(f'books:{user_id}', 3600, json.dumps(books))  # Cache for 1 hour
    
    return jsonify(books)

@books_bp.route('', methods=['POST'])
def add_book():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401

    verification = verify_token(token)
    if not verification['valid']:
        return jsonify({'error': 'Invalid token'}), 401

    user_id = verification['userId']
    book_data = request.json
    book_data['user_id'] = user_id

    # Validate book data
    required_fields = ['title', 'author', 'isbn']
    for field in required_fields:
        if field not in book_data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        result = Book.create(book_data)
        
        # Invalidate cache
        redis_client.delete(f'books:{user_id}')


        response_data = {
            'message': 'Book added successfully',
            'book': {
                'id': str(result.inserted_id),
                **book_data
            }
        }
        
        # Use the custom JSONEncoder to serialize the response
        return jsonify(json.loads(json.dumps(response_data, cls=JSONEncoder))), 201
  
        
    except Exception as e:
        logger.error(f"Error adding book: {str(e)}")
        return jsonify({'error': f'Error adding book: {str(e)}'}), 500

@books_bp.route('/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': 'No token provided'}), 401

    verification = verify_token(token)
    if not verification['valid']:
        return jsonify({'error': 'Invalid token'}), 401

    user_id = verification['userId']

    result = Book.delete(isbn, user_id)
    if result.deleted_count:
        # Invalidate cache
        redis_client.delete(f'books:{user_id}')
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'error': 'Book not found or you do not have permission to delete it'}), 404
