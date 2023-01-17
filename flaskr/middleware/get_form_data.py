
def get_form_data(request_form, data_entries):
    """
    Derives values of keys listed in data_entries from request_form and presents data as dict 
    :return: dict
    """
    data = {} 
    for entry in data_entries:
        if entry['optional'] and entry['name'] not in request_form.keys():
            data[entry['name']] = None
            continue 
        data[entry['name']] = request_form[entry['name']] 
    return data