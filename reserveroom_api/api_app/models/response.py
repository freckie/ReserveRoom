from flask import jsonify

def ok_response(data):
    return jsonify({
        'status': 200,
        'data': data
    })

def error_response(msg, status):
    return jsonify({
        'status': status,
        'message': msg,
        'data': None
    })