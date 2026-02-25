from flask import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Like, Post
from extensions import db
from utils.responses import error_response, success_response

like_bp = Blueprint("likes", __name__)


#LIKE POST
@like_bp.route("/posts/<int:post_id>/like", methods=["POST"])
@jwt_required()
def like_post(post_id):
    user_id = int(get_jwt_identity())

    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    existing_like = Like.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if existing_like:
        return error_response("Post already liked", 400)

    new_like = Like(user_id=user_id, post_id=post_id)
    db.session.add(new_like)
    db.session.commit()

    return success_response(
        message="Post liked"
    ), 201


# UNLIKE POST
@like_bp.route("/posts/<int:post_id>/like", methods=["DELETE"])
@jwt_required()
def unlike_post(post_id):
    user_id = int(get_jwt_identity())

    like = Like.query.filter_by(
        user_id=user_id,
        post_id=post_id
    ).first()

    if not like:
        abort(404)

    db.session.delete(like)
    db.session.commit()

    return success_response(
        message="Post unliked"
    )


# GET LIKES COUNT
@like_bp.route("/posts/<int:post_id>/likes-count", methods=["GET"])
def get_likes_count(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    likes_count = Like.query.filter_by(post_id=post_id).count()

    return success_response(
        message="Likes fetched",
        data={
            "post_id": post_id,
            "likes": likes_count
        }
    )