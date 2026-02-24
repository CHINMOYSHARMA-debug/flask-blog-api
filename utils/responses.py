from flask import jsonify

def success_response(message="Success", status_code=200, data=None):
    res = {
        "success": True,
        "message": message
    }

    if data:
        res["data"] = data
    
    return jsonify(res), status_code


def error_response(message="Error", status_code=400):
    return jsonify({
        "success": False,
        "error": message
    }), status_code