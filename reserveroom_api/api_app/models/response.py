def ok_response(data):
    return {
        'status': 200,
        'message': 'success',
        'data': data
    }

def error_response(msg, status):
    return {
        'status': status,
        'message': msg,
        'data': None
    }