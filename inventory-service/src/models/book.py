# inventory-service/src/models/book.py
from config.database import books_collection

class Book:
    @staticmethod
    def create(book_data):
        return books_collection.insert_one(book_data)

    @staticmethod
    def find_by_user(user_id):
        return books_collection.find({'user_id': user_id})

    @staticmethod
    def find_by_isbn(isbn, user_id):
        return books_collection.find_one({'isbn': isbn, 'user_id': user_id})

    @staticmethod
    def delete(isbn, user_id):
        return books_collection.delete_one({'isbn': isbn, 'user_id': user_id})