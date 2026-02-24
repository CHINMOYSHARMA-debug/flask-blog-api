from flask import jsonify

def success_response(message="Success", status_code=200, data=None):
    response = {
        "success": True,
        "message": message,
    }

    if data:
        response["data"] = data
    
    return jsonify(response), status_code


def error_response(message="Error", status_code=400):
    return jsonify({
        "success": False,
        "error": message
    }), status_code