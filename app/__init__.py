from flask import Flask 


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Register blueprints 
    from .auth import auth 
    app.register_blueprint(auth)

    from .bookmarks import bookmarks
    app.register_blueprint(bookmarks)  



    return app