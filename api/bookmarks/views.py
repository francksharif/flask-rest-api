from flask import request, jsonify
from . import bookmarks
from ..models import Bookmark
from ..constants.http_status_code import *
from flask_jwt_extended import get_jwt_identity 
from flask_jwt_extended.view_decorators import jwt_required
from flasgger import swag_from
from .. import db
import validators



# Create a new Bookmark 
@bookmarks.route('/', methods=['POST'])
@jwt_required()
@swag_from('./docs/post_bookmark.yaml')
def create_bookmark():
    current_user = get_jwt_identity()
    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')
    
    if not validators.url(url):
        return jsonify({
            'error': 'Enter a valid URL'
        }), 400
    
    if Bookmark.query.filter_by(url=url).first():
        return jsonify({
            'error': 'URL already exists'
        }), 409
    
    bookmark = Bookmark(url=url, body=body, user_id=current_user)
    db.session.add(bookmark)
    db.session.commit()

    return jsonify({
        'id': bookmark.id,
        'url': bookmark.url,
        'body': bookmark.body,
        'created_at': bookmark.created_at,
        'updated_at': bookmark.updated_at
    }), 201


    
# Retrieve all Bookmarks
@bookmarks.route('/', methods=['GET'])
@jwt_required()
@swag_from('./docs/get_bookmarks.yaml')
def get_bookmarks():
    current_user = get_jwt_identity()
    page = request.args.get('page', 1, type=int)
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

    meta = {
        "page": bookmarks.page,
        'pages': bookmarks.pages,
        'total_count': bookmarks.total,
        'prev_page': bookmarks.prev_num,
        'next_page': bookmarks.next_num,
        'has_next': bookmarks.has_next,
        'has_prev': bookmarks.has_prev
    }

    return jsonify({'data': data, 'meta': meta}), 200




# Retrieve one bookmark
@bookmarks.route('/<int:id>')
@jwt_required()
@swag_from('./docs/get_bookmark.yaml')
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


# Editing bookmark
@bookmarks.route('/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@swag_from('./docs/edit_bookmark.yaml')
def edit_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()
       
    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    body = request.get_json().get('body', '')
    url = request.get_json().get('url', '')
        
    if not validators.url(url):
            return jsonify({
                'error': 'Enter a valid URL'
            }), HTTP_400_BAD_REQUEST
        
    bookmark.url = url
    bookmark.body = body 
    db.session.commit()

    return jsonify({
            'id': bookmark.id,
            'url': bookmark.url,
            'body': bookmark.body,
            'created_at': bookmark.created_at,
            'updated_at': bookmark.updated_at
        }), HTTP_200_OK



# Deleting a bookmark
@bookmarks.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from('./docs/delete_bookmark.yaml')
def delete_bookmark(id):
    current_user = get_jwt_identity()
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({'message': 'Item not found'}), HTTP_404_NOT_FOUND
    
    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT