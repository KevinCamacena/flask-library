from flask_restful import Resource, reqparse
from .models import Book
from . import db

book_parser = reqparse.RequestParser()
book_parser.add_argument('title', type=str, required=True, help='Title is required')
book_parser.add_argument('author', type=str, required=True, help='Author is required')
book_parser.add_argument('publisher', type=str)
book_parser.add_argument('publication_year', type=int)
book_parser.add_argument('isbn', type=str)
book_parser.add_argument('genre', type=str)
book_parser.add_argument('language', type=str)
book_parser.add_argument('page_count', type=int)
book_parser.add_argument('edition', type=str)
book_parser.add_argument('format', type=str)
book_parser.add_argument('description', type=str)
book_parser.add_argument('availability_status', type=str)
book_parser.add_argument('tags', type=str)

class BookListResource(Resource):
    def get(self):
        books = Book.query.all()
        return [book.to_dict() for book in books], 200

    def post(self):
        args = book_parser.parse_args()
        book = Book(**args)
        db.session.add(book)
        db.session.commit()
        return book.to_dict(), 201

class BookResource(Resource):
    def get(self, id):
        book = Book.query.get_or_404(id)
        return book.to_dict(), 200

    def put(self, id):
        book = Book.query.get_or_404(id)
        args = book_parser.parse_args()
        for key, value in args.items():
            setattr(book, key, value)
        db.session.commit()
        return book.to_dict(), 200

    def delete(self, id):
        book = Book.query.get_or_404(id)
        db.session.delete(book)
        db.session.commit()
        return {'message': 'Book deleted'}, 200
