from flask import Flask 
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)

    # Register blueprints 
    from .auth import auth 
    app.register_blueprint(auth)

    from .bookmarks import bookmarks
    app.register_blueprint(bookmarks)  

    # Register models
    with app.app_context():
        from . import models



    return app