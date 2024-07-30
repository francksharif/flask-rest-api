from datetime import datetime
import os
import string
import random
import pyshorteners
from flask_sqlalchemy import SQLAlchemy
from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False )
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    
    # Foreign key relationship
    bookmarks = db.relationship('Bookmark', backref='User')


    def __repr__(self) -> str:
        return 'User -> ' f'{self.username}'
    


class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text(), nullable=False)
    short_url = db.Column(db.String(30), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # Foreign key
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        s = pyshorteners.Shortener(os.environ.get('SHORTCM_KEY'))
        self.short_url = s.shortcm.short(self.url)

    def __repr__(self) -> str:
        return 'User -> ' f'{self.url}'
    
    