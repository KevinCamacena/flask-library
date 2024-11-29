class Book:
    def __init__(self, title, author, publication_year, book_id=None):
        self.id = book_id
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"
