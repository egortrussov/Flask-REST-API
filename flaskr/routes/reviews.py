from flask import Blueprint, request, jsonify

from ..db.db import create_session
from ..models.Order import Order 
from ..models.User import User 
from ..models.Review import Review

from ..middleware.token_validation import token_required
from ..middleware.auth_middleware import generate_id
from ..middleware.request_validation import form_data_required
from ..middleware.get_form_data import get_form_data

from .request_requirements.reviews_requirements import CREATE_REVIEW_DATA

bp = Blueprint('reviews', __name__, url_prefix='/api/reviews')

@bp.route('/createReview', methods=['POST']) 
@form_data_required(CREATE_REVIEW_DATA)
@token_required 
def create_review(decoded_token=None):
    session = create_session() 

    review_data = get_form_data(request.form, CREATE_REVIEW_DATA)
    review_data['review_id'] = generate_id()
    review_data['author_id'] = decoded_token['user_id']

    order = session.query(Order).filter_by(order_id=review_data['order_id']).first() 

    if order is None:
        return { 'success': False, 'error': 'Order not found' }, 400  
    if not order.completed or not order.assigned_to:
        return { 'success': False, 'error': 'Unable to create review' }, 400 
    
    new_review = Review(**review_data) 

    session.add(new_review) 
    session.commit()

    return {
        'success': True
    }, 200

