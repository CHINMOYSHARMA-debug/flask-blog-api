from app.utils.responses import error_response
from app.models import TokenBlockList
from app.extensions import db, jwt

def register_jwt_handlers(app):
    
    @jwt.token_in_blocklist_loader
    def check_in_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()
        return token is not None

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return error_response("Token has expired", 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return error_response("Invalid token", 401)

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return error_response("Authorization token required", 401)