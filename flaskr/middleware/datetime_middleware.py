def str_to_datetime_data(date):
    """
    Converts date data from string to dict type
    :return: dict
    """
    yy_mm_dd, hh_mm_ss = date.split(' ') 
    yy_mm_dd = yy_mm_dd.split('-')
    hh_mm_ss = hh_mm_ss.split(':')  
    return {
        'year': int(yy_mm_dd[0]),
        'month': int(yy_mm_dd[1]),
        'day': int(yy_mm_dd[2]),
        'hour': int(hh_mm_ss[0]),
        'minute': int(hh_mm_ss[1]),
        'second': int(hh_mm_ss[2]),
        'microsecond': 0
    }

def check_intersection(timestamps_list, timestamp):
    """
    Checks is timestamp intersects with any of timestamps in timestamps_list 
    :return: bool
    """
    for ts in timestamps_list:
        print(ts[0], timestamp[0])
        if max(ts[0], timestamp[0]) < min(ts[1], timestamp[1]):
            return True 
    return False