from flask import Flask
from dotenv import load_dotenv
from app.config import Config
from app.extensions import db, bcrypt, jwt, limiter
from flask_cors import CORS
from flask_migrate import Migrate
from flasgger import Swagger
from app.utils.jwt_handlers import register_jwt_handlers
from app.utils.error_handlers import register_error_handlers
from app.logging.logging_config import setup_logging
import os

from app.routes.auth_routes import auth_bp
from app.routes.post_routes import post_bp
from app.routes.comment_routes import comment_bp
from app.routes.like_routes import like_bp
from app.routes.user_routes import user_bp
from app.routes.main_routes import main_bp


def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    env = os.getenv("FLASK_ENV", "development")

    if env == "production":
        app.config.from_object("app.config.Productionconfig")
    else:
        app.config.from_object("app.config.DevelopmentConfig")
        
    #config
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    setup_logging()
    
    #extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    
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
    
    Swagger(app)

    return app

