import os
from flasgger import Swagger, swag_from


base_dir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    SWAGGER={
        'title': 'Flask REST API',
        'uiversion': 3
    }