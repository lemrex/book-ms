from flask import Flask
from routes.books import books_bp
from config.database import init_db
from flask_cors import CORS  # Import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, resources={r"/*": {"origins": "*"}})


# Initialize database
# init_db()

# Register blueprintss
app.register_blueprint(books_bp, url_prefix='/books')

if __name__ == '__main__':
    app.run(port=3001)
