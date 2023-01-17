from flask import Blueprint, request, jsonify

from ..db.db import create_session
from ..models.User import User

from ..middleware import auth_middleware
from ..middleware.request_validation import form_data_required
from ..middleware.get_form_data import get_form_data

from .request_requirements.auth_requirements import LOGIN_DATA, REGISTER_DATA 

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/register', methods=['POST']) 
@form_data_required(REGISTER_DATA)
def register():
    """ 
    Adds user credentials to the database 
    :return: { 
        success: bool  
        error: string  
    }
    """
    session = create_session()

    creds = get_form_data(request.form, REGISTER_DATA)
    
    existing_user = session.query(User).filter_by(username=creds['username']).first() 

    if existing_user:
        return { 'success': 'False', 'error': 'Username already exists' }, 400
    
    creds['user_id'] = auth_middleware.generate_id() 
    creds['password'] = auth_middleware.generate_password_hash(creds['password'])

    new_user = User(**creds) 
    session.add(new_user) 
    session.commit()

    return { 'success': 'True' }, 200 

@bp.route('/login', methods=['POST']) 
@form_data_required(LOGIN_DATA)
def login():
    """
    Checks user credentials, generates auth token 
    :return: {
        success: bool 
        error: string 
        user: dict 
        token: string
    }
    """
    session = create_session()

    creds = get_form_data(request.form, LOGIN_DATA)

    user = session.query(User).filter_by(username=creds['username']).first()
    
    if not user:
        return { 'success': False, 'error': 'User not found' }

    if not user.check_password_hash(creds['password']):
        return { 'success': False, 'error': 'Incorrect password' }, 400 
    

    token = user.encode_auth_token()

    return {
        'success': True,
        'user': user.get_user_data_as_dict(),
        'token': token
    }, 200


