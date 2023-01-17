from flask import Blueprint, request
import datetime

from ..middleware.token_validation import token_required 
from ..middleware.auth_middleware import generate_id
from ..middleware.datetime_middleware import str_to_datetime_data, check_intersection
from ..middleware.get_form_data import get_form_data
from ..middleware.request_validation import form_data_required, request_args_required

from ..db.db import create_session 
from ..models.Order import Order
from ..models.User import User

from .request_requirements.order_requirements import CREATE_ORDER_DATA, ORDER_DATA_ARGS, DELETE_ORDER_ARGS, ASSIGN_ORDER_ARGS, COMPLETE_ORDER_ARGS

bp = Blueprint('orders', __name__, url_prefix='/api/orders')

@bp.route('/createOrder', methods=('POST',)) 
@form_data_required(CREATE_ORDER_DATA)
@token_required
def create_order(decoded_token=None):
    session = create_session() 

    order_data = get_form_data(request.form, CREATE_ORDER_DATA)
    order_data['created_by'] = decoded_token['user_id']
    order_data['completed'] = 0 
    order_data['assigned_to'] = None
    order_data['order_id'] = generate_id() 
    order_data['time_start'] = datetime.datetime(**str_to_datetime_data(order_data['time_start']))
    order_data['time_finish'] = datetime.datetime(**str_to_datetime_data(order_data['time_finish']))
    
    new_order = Order(**order_data) 
    session.add(new_order) 
    session.commit()

    return {
        'success': True,
        'order_data': order_data 
    }, 200

@bp.route('/orderData', methods=('GET', )) 
@request_args_required(ORDER_DATA_ARGS)
@token_required
def order_data(decoded_token=None):
    session = create_session() 
    
    order = session.query(Order).filter_by(order_id=request.args['order_id']).first() 

    if order is None:
        return { 'success': False, 'error': 'Order not found' }, 400 
    
    if decoded_token['user_id'] != order.created_by and not decoded_token['is_worker']:
        return { 'success': False, 'error': 'Access to order denied' }, 400 
    
    return {
        'success': True,
        'order_data': order.get_order_data_as_dict()
    } 

@bp.route('/deleteOrder', methods=('DELETE', )) 
@request_args_required(DELETE_ORDER_ARGS)
@token_required
def delete_order(decoded_token=None):
    session = create_session() 
    
    order = session.query(Order).filter_by(order_id=request.args['order_id']).first() 

    if order is None:
        return { 'success': False, 'error': 'Order not found' }, 400 
    
    if decoded_token['user_id'] != order.created_by or order.completed:
        return { 'success': False, 'error': 'Not allowed to delete the order' }, 400 
    
    session.delete(order) 
    session.commit()
    
    return {
        'success': True 
    } 

@bp.route('/assignOrder', methods=['PATCH']) 
@request_args_required(ASSIGN_ORDER_ARGS)
@token_required 
def assign_order(decoded_token=None):
    session = create_session() 
    
    # get worker data from database
    worker = session.query(User).filter_by(user_id=request.args['worker_id']).first() 

    if worker is None:
        return { 'success': False, 'error': 'worker not found' }, 400 
    if not worker.is_worker:
        return { 'success': False, 'error': 'Order must be assigned to a worker' }, 400 
    
    # get order data from database
    order = session.query(Order).filter_by(order_id=request.args['order_id']).first() 

    if order is None:
        return { 'success': False, 'error': 'Order not found' }, 400 
    
    if decoded_token['user_id'] != order.created_by or order.completed:
        return { 'success': False, 'error': 'Not allowed to assign the order' }, 400  
    
    if order.assigned_to == request.args['worker_id']:
        return { 'success': True }, 200
    
    timestamps = worker.get_assigned_orders_timestamps() 

    current_timestamp = (order.time_start, order.time_finish)

    if check_intersection(timestamps, current_timestamp):
        return { 'success': False, 'error': 'Order intersects with an already assigned order' }, 400 
    
    order.assigned_to = request.args['worker_id'] 
    session.commit()

    return {
        'success': True
    }
    
@bp.route('/completeOrder', methods=['PATCH']) 
@request_args_required(COMPLETE_ORDER_ARGS)
@token_required 
def complete_order(decoded_token=None):
    session = create_session() 
    
    order = session.query(Order).filter_by(order_id=request.args['order_id']).first() 

    if order is None:
        return { 'success': False, 'error': 'Order not found' }, 400 
    
    if order.assigned_to != decoded_token['user_id'] and order.created_by != decoded_token['user_id'] or order.completed:
        return { 'success': False, 'error': 'Not allowed to complete order' }, 400 

    order.completed = 1 
    session.commit() 
    
    return { 'success': True }, 200
    