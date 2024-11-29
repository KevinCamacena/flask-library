# views.py
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from dotenv import dotenv_values

config = dotenv_values(".env")
URI = f"mysql+pymysql://{config['MYSQL_ROOT']}:{config['MYSQL_ROOT_PASSWORD']}@localhost:3306/{config['MYSQL_DATABASE']}"
app = Flask(__name__)
app.config['SECRET_KEY'] = config['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = URI
db = SQLAlchemy(app)

# Initialize CSRF protection
csrf = CSRFProtect(app)

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

# Optional: Define a Flask-WTF form for better form handling
class BookForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    publisher = StringField('Publisher', validators=[DataRequired(), Length(max=255)])
    publication_year = IntegerField('Publication Year', validators=[DataRequired()])
    isbn = StringField('ISBN', validators=[DataRequired(), Length(max=20)])
    genre = StringField('Genre', validators=[Length(max=100)])
    language = StringField('Language', validators=[Length(max=50)])
    page_count = IntegerField('Page Count')
    edition = StringField('Edition', validators=[Length(max=50)])
    format = StringField('Format', validators=[Length(max=50)])
    description = TextAreaField('Description')
    availability_status = StringField('Availability Status', validators=[Length(max=50)])
    tags = TextAreaField('Tags')
    submit = SubmitField('Save Changes')

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(obj=book)  # Populate form with book data

    if form.validate_on_submit():
        form.populate_obj(book)  # Update book object with form data
        try:
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('some_view'))  # Replace 'some_view' with your target view
        except Exception as e:
            db.session.rollback()
            flash('Error updating book.', 'danger')

    return render_template('edit_book.html', form=form, book=book)

if __name__ == '__main__':
    app.run(debug=True)