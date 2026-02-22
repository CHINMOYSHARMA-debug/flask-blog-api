from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User
from utils.responses import error_response, success_response

user_bp = Blueprint("user_bp", __name__)

@user_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user_profiel(user_id):

    user = db.session.get(User, user_id)

    if not user:
       abort(404)
    
    return success_response({
        "id" : user_id,
        "username" : user.username,
        "bio" : user.bio,
        "profile_pic" : user.profile_pic
    })

@user_bp.route("/users/me", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)

    user =  db.session.get(User, user_id)

    if not user:
       abort(404)

    bio = data.get("bio")
    profile_pic = data.get("profile_pic")

    if bio is not None:
        user.bio = bio
    
    if profile_pic is not None:
        user.profile_pic = profile_pic

    db.session.commit()

    return success_response({
        "message": "Profile updated",
        "user": {
            "id" : user.id,
            "username": user.username,
            "bio": user.bio,
            "profile_pic": user.profile_pic
        }
    })