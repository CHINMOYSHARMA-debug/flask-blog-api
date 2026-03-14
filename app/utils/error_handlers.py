from app.utils.responses import error_response
from flask_limiter.errors import RateLimitExceeded
from flask import jsonify

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return error_response("Resource not found", 404)

    @app.errorhandler(400)
    def bad_request(e):
        return error_response("Bad request", 400)

    @app.errorhandler(403)
    def forbidden(e):
        return error_response("Forbidden", 403)

    @app.errorhandler(500)
    def server_error(e):
        print("ERROR:", e)
        return error_response("Internal server response", 500)
    
    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        return jsonify({
            "error": "Too many requests",
            "message": "Rate limit exceeded"
        }), 429