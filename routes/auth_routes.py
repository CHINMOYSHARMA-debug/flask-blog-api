from flask_jwt_extended import (
    jwt_required,
    get_jwt,
    get_jwt_identity,
    create_access_token,
    create_refresh_token
)
from flask import Blueprint, request, abort
from models import User, TokenBlockList
from extensions import db, bcrypt
from datetime import datetime
from utils.responses import error_response, success_response

auth_bp = Blueprint("auth", __name__)

# REGISTER
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True)

    if data is None:
        return error_response("Request body must be JSON", 400)
    if not data.get("username"):
        return error_response("Username is required", 400)
    if not data.get("password"):
        return error_response("Password is required", 400)
    if not data.get("email"):
        return error_response("Email is required", 400)
     
    existing_user = User.query.filter_by(username=data["username"]).first()
    
    if existing_user:
        return error_response("Username already exists", 400)
    
    existing_mail = User.query.filter_by(email=data["email"]).first()

    if existing_mail:
        return error_response("Email already exists", 400)

    hashed_password = bcrypt.generate_password_hash(
        data["password"]
    ).decode("utf-8")

    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()
    return success_response("User created", 201)


# LOGIN
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)
    if not data.get("username"):
        return error_response("Username is required", 400)
    if not data.get("password"):
        return error_response("Password is required", 400)

    user = User.query.filter_by(username=data["username"]).first()

    if not user or not bcrypt.check_password_hash(user.password, data["password"]):
        return error_response("Invalid username or password", 401)

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return success_response(
        message="Login successful",
        data={
            "access token": access_token,
            "refresh_token": refresh_token
        }
    )

# LOGOUT (token revocation)
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jwt_data = get_jwt()
    jti = jwt_data["jti"]

    revoked_token = TokenBlockList(
        jti=jti,
        created_at=datetime.utcnow()
    )

    db.session.add(revoked_token)
    db.session.commit()

    return success_response(message="Successfully logged out")


# GET CURRENT USER
@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)

    if not user:
        abort(404)
    return success_response(
        message="User fetched",
        data={
            "id": user.id,
            "username": user.username,
            "email": user.email   
        }
    )

# REFRESH TOKEN
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)

    return success_response({
        "access_token": new_access_token
    })

# CHANGE PASSWORD
@auth_bp.route("/change-password", methods=["PUT"])
@jwt_required()
def change_password():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return error_response("Both old and new passwords required", 400)

    user = db.session.get(User, user_id)

    if not user:
        abort(404)

    if not bcrypt.check_password_hash(user.password, old_password):
        return error_response("Old password is incorrect", 401)

    new_hash = bcrypt.generate_password_hash(new_password).decode("utf-8")
    user.password = new_hash

    db.session.commit()

    return success_response(message="Password updated successfully")