from flask import Blueprint

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def home():
    return {
        "message": "Flask Blog API is running",
        "docs": "/docs",
        "endpoints": [
            "/register",
            "/login",
            "/posts"
        ]
    }
