from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from api.constants.http_status_code import *
from api.config.swagger import template, swagger_config
from flasgger import Swagger

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    jwt.init_app(app)

    # Register blueprints 
    from .auth import auth 
    app.register_blueprint(auth)

    from .bookmarks import bookmarks
    app.register_blueprint(bookmarks)  

    # Swagger config 
    Swagger(app, config=swagger_config, template=template)

    # Register models
    with app.app_context():
        from . import models

    # Error Handlers
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def error_404(e):
        return jsonify({'error': 'Not Found'}), HTTP_404_NOT_FOUND
    
    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def error_404(e):
        return jsonify({'error': 'Something went wrong, we are working on it'}), HTTP_500_INTERNAL_SERVER_ERROR


    return app