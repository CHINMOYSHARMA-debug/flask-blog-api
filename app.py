from flask import Flask
from extensions import db, bcrypt, jwt
from models import User, Post, TokenBlockList, Comment, Like
from flask_jwt_extended import JWTManager

from routes.auth_routes import auth_bp
from routes.post_routes import post_bp
from routes.comment_routes import comment_bp
from routes.like_routes import like_bp
from routes.user_routes import user_bp
from utils.responses import error_response
from flasgger import Swagger
from flask_migrate import Migrate

app = Flask(__name__)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "OK"

swagger_config = {
    "headers" : [],
    "specs" : [
        {
            "endpoint" : 'apispec',
            "route" : '/apispec.json',
            "rule_filter" : lambda rule: True,
            "model_filter" : lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/"
}

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Flask Blog API",
        "version": "1.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter: Bearer <your_token>"
        }
    },
    "security": [
        {
            "Bearer": []
        } 
    ]
}

jwt = JWTManager(app)

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return error_response("Token has expired", 401)

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return error_response("Invalid token", 401)

@jwt.unauthorized_loader
def missing_token_callback(error):
    return error_response("Authorization token required", 401)

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
    return error_response("Internal server response", 500)

# Config
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

uri = os.getenv("DATABASE_URL")

if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

if not uri:
    raise ValueError("DATABASE_URL is not set!")

if "sslmode" not in uri:
    uri += "?sslmode=require"

print("USING DB:", uri)

app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["headers"]

app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]

from datetime import timedelta

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

#Extensions initialize
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)


with app.app_context():
    db.create_all()

#Token Revocation Checker
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]  # unique token id

    token = db.session.query(TokenBlockList.id).filter_by(jti=jti).scalar()

    return token is not None

app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)
app.register_blueprint(comment_bp) 
app.register_blueprint(like_bp)
app.register_blueprint(user_bp)

Swagger(app, config=swagger_config, template=swagger_template)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

