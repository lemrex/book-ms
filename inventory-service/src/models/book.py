# # inventory-service/src/models/book.py
# from src.config.database import books_collection

# class Book:
#     @staticmethod
#     def create(book_data):
#         return books_collection.insert_one(book_data)

#     @staticmethod
#     def find_by_user(user_id):
#         return books_collection.find({'user_id': user_id})

#     @staticmethod
#     def find_by_isbn(isbn, user_id):
#         return books_collection.find_one({'isbn': isbn, 'user_id': user_id})

#     @staticmethod
#     def delete(isbn, user_id):
#         return books_collection.delete_one({'isbn': isbn, 'user_id': user_id})


from src.config.database import MongoDBHandler

class Book:
    @staticmethod
    def create(book_data):
        with MongoDBHandler().get_connection() as mongo:
            return mongo.books_collection.insert_one(book_data)

    @staticmethod
    def find_by_user(user_id):
        with MongoDBHandler().get_connection() as mongo:
            return mongo.books_collection.find({'user_id': user_id})

    @staticmethod
    def find_by_isbn(isbn, user_id):
        with MongoDBHandler().get_connection() as mongo:
            return mongo.books_collection.find_one({'isbn': isbn, 'user_id': user_id})

    @staticmethod
    def delete(isbn, user_id):
        with MongoDBHandler().get_connection() as mongo:
            return mongo.books_collection.delete_one({'isbn': isbn, 'user_id': user_id})
