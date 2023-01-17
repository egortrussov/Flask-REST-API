USER_DATA_ARGS = [
    {
        'name': 'user_id',
        'optional': False,
    }
    
] 

CREATED_ORDERS_ARGS = [
    {
        'name': 'user_id',
        'optional': False,
    }
]

ASSIGNED_ORDERS_ARGS = [
    {
        'name': 'user_id',
        'optional': False,
    }
]

GET_AVAILABLE_WORKERS_DATA = [
    {
        'name': 'time_start',
        'optional': False,
    },
    {
        'name': 'time_finish',
        'optional': False,
    },
    
]

WORKER_GRADES_ARGS = [
    {
        'name': 'worker_id',
        'optional': False
    }
]