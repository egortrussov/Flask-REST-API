from flask import request

def form_data_required(data_entries):
    """
    Checks if request.form has all the keys listed in data_entries, returns error is keys are missing 
    """
    def decorator(route_function):
        def wrapper():
            missing_entries = []
            for entry in data_entries:
                if entry['name'] not in request.form.keys() and not entry['optional']:
                    missing_entries.append(entry['name']) 
            if len(missing_entries):
                return {
                    'success': False,
                    'error': ', '.join(missing_entries) + ' are missing in request form data'
                }, 400
            return route_function()
        wrapper.__name__ = route_function.__name__
        return wrapper
    return decorator

def request_args_required(data_entries):
    """
    Checks if request.args has all the keys listed in data_entries, returns error is keys are missing 
    """
    def decorator(route_function):
        def wrapper():
            missing_entries = []
            for entry in data_entries:
                if entry['name'] not in request.args.keys() and not entry['optional']:
                    missing_entries.append(entry['name']) 
            if len(missing_entries):
                return {
                    'success': False,
                    'error': ', '.join(missing_entries) + ' are missing in request arguments'
                }, 400
            return route_function()
        wrapper.__name__ = route_function.__name__
        return wrapper
    return decorator

