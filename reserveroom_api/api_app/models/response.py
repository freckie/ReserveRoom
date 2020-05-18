def ok_response(data):
    return {
        'status': 200,
        'message': 'success',
        'data': data
    }

def error_response(status, msg):
    return {
        'status': status,
        'message': msg,
        'data': None
    }