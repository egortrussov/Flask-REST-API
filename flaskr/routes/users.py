from flask import Blueprint, request
from datetime import datetime

from ..middleware.token_validation import token_required 
from ..middleware.request_validation import request_args_required 
from ..middleware.datetime_middleware import check_intersection, str_to_datetime_data

from ..db.db import create_session 
from ..models.User import User 

from .request_requirements.users_requirements import CREATED_ORDERS_ARGS, USER_DATA_ARGS, ASSIGNED_ORDERS_ARGS, GET_AVAILABLE_WORKERS_ARGS, WORKER_GRADES_ARGS

bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/userData', methods=('GET',)) 
@request_args_required(USER_DATA_ARGS)
@token_required
def user_data(decoded_token=None):
    session = create_session() 

    user_id = request.args['user_id'] 

    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        return { 'success': False, 'error': 'User not found' }
    
    return {
        'user_data': user.get_user_data_as_dict(),
        'success': True,
    }

@bp.route('/createdOrders', methods=('GET',)) 
@request_args_required(CREATED_ORDERS_ARGS)
@token_required
def created_orders(decoded_token=None):
    session = create_session() 

    user_id = request.args['user_id'] 
    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        return { 'success': False, 'error': 'User not found' }
    
    return {
        'created_orders': user.get_created_orders(),
        'success': True,
    }

@bp.route('/assignedOrders', methods=('GET',)) 
@request_args_required(ASSIGNED_ORDERS_ARGS)
@token_required
def assigned_orders(decoded_token=None):
    session = create_session() 

    user_id = request.args['user_id'] 

    user = session.query(User).filter_by(user_id=user_id).first()

    if not user:
        return { 'success': False, 'error': 'User not found' }
    
    return {
        'assigned_orders': user.get_assigned_orders(),
        'success': True,
    }

@bp.route('/availableWorkers', methods=['GET', ]) 
@request_args_required(GET_AVAILABLE_WORKERS_ARGS)
def get_available_workers():
    session = create_session() 

    timestamp = (
        datetime(**str_to_datetime_data(request.args['time_start'])), 
        datetime(**str_to_datetime_data(request.args['time_finish']))
    )
    available_workers = []

    workers = session.query(User).filter_by(is_worker=True).all() 

    for worker in workers:
        assigned_orders_timestamps = worker.get_assigned_orders_timestamps() 
        if not check_intersection(assigned_orders_timestamps, timestamp):
            available_workers.append(worker.user_id) 
    
    return {
        'success': True,
        'available_workers': available_workers
    }

@bp.route('/workerGrades', methods=['GET']) 
@request_args_required(WORKER_GRADES_ARGS)
def worker_grades():
    session = create_session() 

    worker_id = request.args['worker_id'] 

    user = session.query(User).filter_by(user_id=worker_id).first() 

    if not user:
        return {
            'success': False,
            'error': 'User not found'
        }, 400
    if not user.is_worker:
        return {
            'success': False,
            'error': 'User is not a worker'
        }, 400
    
    grades = user.get_order_grades() 
    average_grade = 0 if not len(grades) else sum(grades) / len(grades)

    return {
        'success': True,
        'grades': grades,
        'average_grade': average_grade
    }

