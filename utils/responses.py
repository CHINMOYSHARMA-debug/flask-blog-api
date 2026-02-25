from flask import jsonify

def success_response(message=None, data=None):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    })

def error_response(message="Error", status_code=400):
    return jsonify({
        "success": False,
        "error": message
    }), status_code