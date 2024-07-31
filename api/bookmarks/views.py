from flask import request, jsonify
from . import bookmarks
from ..models import Bookmark
from ..constants.http_status_code import *
from flask_jwt_extended import get_jwt_identity 
from flask_jwt_extended.view_decorators import jwt_required
from .. import db
import validators

# Create a new Bookmark and Retrieve all Bookmarks
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
        page = request.args.get('page',1,type=int)
        per_page = request.args.get('per_page', 5, type=int)

        bookmarks = Bookmark.query.filter_by(
            user_id=current_user).paginate(page=page, per_page=per_page)


        data = []
        for bookmark in bookmarks.items:
            data.append({
            'id': bookmark.id,
            'url': bookmark.url,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
            })

        meta={
            "page": bookmarks.page,
            'pages': bookmarks.page,
            'total_count': bookmarks.total,
            'prev_page': bookmarks.prev_num,
            'next_page': bookmarks.next_num,
            'has_next': bookmarks.has_next,
            'has_prev': bookmarks.has_prev
        }

        return jsonify({'data':data, 'meta': meta}), HTTP_200_OK


# Retrieve one bookmark
@bookmarks.route('/<int:id>')
@jwt_required()
def get_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
    
    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
    }), HTTP_200_OK