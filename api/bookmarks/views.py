from flask import request, jsonify
from . import bookmarks
from ..models import Bookmark
from ..constants.http_status_code import *
from flask_jwt_extended import get_jwt_identity 
from flask_jwt_extended.view_decorators import jwt_required
from .. import db
import validators

# Create a new Bookmark
@bookmarks.route('/', methods=['GET', 'POST'])
@jwt_required()
def handle_bookmarks():
    current_user = get_jwt_identity()
    if request.method == 'POST':
        body = request.get_json().get('body', '')
        url = request.get_json().get('url', '')
        
        if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid URL'
            }), HTTP_400_BAD_REQUEST
        
        if Bookmark.query.filter_by(url=url).first():
             return jsonify({
                'error': 'URL already exists'
            }), HTTP_400_BAD_REQUEST
        
        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), HTTP_201_CREATED

    else:
        bookmarks = Bookmark.query.filter_by(user_id=current_user)
        data = []
        for bookmark in bookmarks:
            data.append({
            'id': bookmark.id,
            'url': bookmark.url,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
            })
        return jsonify({'data':data}), HTTP_200_OK

