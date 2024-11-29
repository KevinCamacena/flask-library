from . import db

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(20), nullable=False)
    genre = db.Column(db.String(100))
    language = db.Column(db.String(50))
    page_count = db.Column(db.Integer)
    edition = db.Column(db.String(50))
    format = db.Column(db.String(50))
    description = db.Column(db.Text)
    availability_status = db.Column(db.String(50))
    tags = db.Column(db.Text)

    def __str__(self):
        return f"{self.title} by {self.author}"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'publisher': self.publisher,
            'publication_year': self.publication_year,
            'isbn': self.isbn,
            'genre': self.genre,
            'language': self.language,
            'page_count': self.page_count,
            'edition': self.edition,
            'format': self.format,
            'description': self.description,
            'availability_status': self.availability_status,
            'tags': self.tags,
        }
