CREATE_ORDER_DATA = [
    {
        'name': 'title',
        'optional': False
    },
    {
        'name': 'description',
        'optional': True
    },
    {
        'name': 'address_from',
        'optional': False
    },
    {
        'name': 'address_to',
        'optional': False
    },
    {
        'name': 'time_start',
        'optional': False
    },
    {
        'name': 'time_finish',
        'optional': False
    }   
]

ORDER_DATA_ARGS = [
    {
        'name': 'order_id',
        'optional': False
    }
]

DELETE_ORDER_ARGS = [
    {
        'name': 'order_id',
        'optional': False
    }
]

ASSIGN_ORDER_ARGS = [
    {
        'name': 'order_id',
        'optional': False
    },
    {
        'name': 'worker_id',
        'optional': False
    }
]

COMPLETE_ORDER_ARGS = [
    {
        'name': 'order_id',
        'optional': False
    }
]