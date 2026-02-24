from flask import jsonify

def success_response(data=None, message=None, status=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status


def error_response(message="something went wrong", status=400):
    return jsonify({
        "success": False,
        "error": message
    }), status