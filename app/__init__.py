import time
from flask import Flask, g, request
from flask_jwt_extended import get_jwt_identity
from dotenv import load_dotenv
from app.config import Config
from app.extensions import db, bcrypt, jwt, limiter
from flask_cors import CORS
from flask_migrate import Migrate
from flasgger import Swagger
from app.utils.jwt_handlers import register_jwt_handlers
from app.utils.error_handlers import register_error_handlers
from app.utils.logger import setup_logger
import os
from app.routes.auth_routes import auth_bp
from app.routes.post_routes import post_bp
from app.routes.comment_routes import comment_bp
from app.routes.like_routes import like_bp
from app.routes.user_routes import user_bp
from app.routes.main_routes import main_bp
from app.routes.health_routes import health_bp

logger = setup_logger()

def create_app():
    load_dotenv()
    logger.info("LOGGER INITIALIZED")

    app = Flask(__name__)
    app.config.from_object(Config)
    app.logger.handlers = logger.handlers
    app.logger.setLevel(logger.level)
    CORS(
        app,
        resources={r"/*": {"origins": "*"}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.Productionconfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")
        
    #config
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    #extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    @app.before_request
    def start_timer():
        print(">>> BEFORE REQUEST")
        g.start_time = time.time()

    @app.after_request
    def log_request(response):
        
        print(">>> AFTER REQUEST")
        print("METHOD:", request.method)
        print("PATH:"< request.path)

        duration = round((time.time() - g.start_time) * 1000, 2)
       
        print("DURATION:", duration)

        return response
    
    #register jwt handlers
    register_jwt_handlers(app)

    #register error handlers
    register_error_handlers(app)

    migrate = Migrate(app, db)
    
    CORS(app, resources={r"/*": {"origins":"http://127.0.0.1:5500"}})

    #blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp) 
    app.register_blueprint(like_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(health_bp)
    
    Swagger(app)

    return app

