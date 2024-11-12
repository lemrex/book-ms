# src/middleware/auth.py
import jwt
from functools import wraps
from flask import request, jsonify
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET_KEY')  # Should match the Auth Service secret

def authenticateJWT(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403

        try:
            token = token.split(" ")[1]  # Remove 'Bearer ' prefix
            jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            return jsonify({'message': 'Token is invalid!'}), 403

        return f(*args, **kwargs)
    
    return decorated
