from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from models import Book

app = Flask(__name__)
DATABASE = "library.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# Home route: List all books
@app.route("/")
def index():
    conn = get_db_connection()
    books = conn.execute("SELECT * FROM books").fetchall()
    conn.close()
    return render_template("index.html", books=books)


# Add a new book
@app.route("/add", methods=("GET", "POST"))
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["publication_year"]

        conn = get_db_connection()
        conn.execute(
            "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)",
            (title, author, year),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))
    return render_template("add_book.html")


# Update an existing book
@app.route("/edit/<int:book_id>", methods=("GET", "POST"))
def edit_book(book_id):
    conn = get_db_connection()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()

    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        year = request.form["publication_year"]

        conn.execute(
            "UPDATE books SET title = ?, author = ?, publication_year = ? WHERE id = ?",
            (title, author, year, book_id),
        )
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn.close()
    return render_template("edit_book.html", book=book)


# Delete a book
@app.route("/delete/<int:book_id>", methods=("POST",))
def delete_book(book_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
