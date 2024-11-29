from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Book
from . import db, socketio


main = Blueprint('main', __name__)

@main.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@main.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        # Extract form data
        new_book = Book(
            title=request.form['title'],
            author=request.form['author'],
            publisher=request.form.get('publisher'),
            publication_year=request.form.get('publication_year'),
            isbn=request.form.get('isbn'),
            genre=request.form.get('genre'),
            language=request.form.get('language'),
            page_count=request.form.get('page_count'),
            edition=request.form.get('edition'),
            format=request.form.get('format'),
            description=request.form.get('description'),
            availability_status=request.form.get('availability_status'),
            tags=request.form.get('tags'),
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('add_book.html')

@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        # Update book details
        book.title = request.form['title']
        book.author = request.form['author']
        # Update other fields as needed
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('main.index'))
    return render_template('edit_book.html', book=book)

@main.route('/delete/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    socketio.emit('book_deleted', {'id': id})
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('main.index'))
