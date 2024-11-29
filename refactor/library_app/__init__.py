from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flask_socketio import SocketIO
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
api = Api()
socketio = SocketIO()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    socketio.init_app(app)

    # Import and register blueprints, resources, and routes
    from .models import Book
    from .resources import BookResource, BookListResource
    from .routes import main as main_blueprint

    app.register_blueprint(main_blueprint)
    api.add_resource(BookListResource, '/api/books')
    api.add_resource(BookResource, '/api/books/<int:id>')

    return app
