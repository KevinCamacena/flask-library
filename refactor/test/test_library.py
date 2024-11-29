import pytest
from library_app import create_app, db
from library_app.models import Book

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_book(client):
    response = client.post('/add', data={
        'title': 'Test Book',
        'author': 'Author Name',
    }, follow_redirects=True)
    assert b'Book added successfully!' in response.data
