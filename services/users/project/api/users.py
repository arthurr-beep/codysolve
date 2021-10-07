from flask import Blueprint, jsonify, request, render_template
from project.api.models import User
from project import db
from sqlalchemy import exc

users_blueprint = Blueprint('users', __name__, template_folder='./templates')

@users_blueprint.route('/users/hello', methods=['GET'])
def hello_hi():
    """ A test Route

    
    """
    return jsonify({
        'status': 'success',
        'message': 'hi you!'
    })

@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response = {
        'status': 'failed',
        'message': 'Invalid request payload.'
    }
    if not post_data:
        return jsonify(response), 400
    
    username = post_data.get('username')
    email = post_data.get('email')
    if not username or not email:
        response['message'] = 'Invalid request payload. One or more missing keys.'
        return jsonify(response), 400

    try:
        user = User.query.filter_by(email=email).first()

        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response['status'] = 'success'
            response['message'] = f'user {email} was added with success.'
            return jsonify(response), 201
        else:
            response['message'] = 'Sorry. That email already exists.'
            return jsonify(response), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response), 400
    
@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """ Get a single user"""  
    response = {
        'status': 'failed',
        'message': 'User does not exist'
    }

    try:
        user_id = int(user_id)
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(response), 404
        else:
            response = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(response), 200
    except ValueError:
        return jsonify(response), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    response = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()]
        }
    } 
    return jsonify(response), 200

@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)
        
    
