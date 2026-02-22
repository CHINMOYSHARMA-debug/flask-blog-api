from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Comment, Post
from extensions import db
from utils.responses import error_response, success_response

comment_bp = Blueprint("comments", __name__)

# ADD COMMENT
@comment_bp.route("/posts/<int:post_id>/comments", methods=["POST"])
@jwt_required()
def add_comment(post_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)

    text = data.get("text")

    if not text or text.strip() == "":
        return error_response("Comment text is required", 400)

    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    new_comment = Comment(
        text=text,
        user_id=user_id,
        post_id=post_id
    )

    db.session.add(new_comment)
    db.session.commit()

    return success_response(
        data=new_comment.to_dict(),
        message="Comment added successfully",
        status=201
    )

# GET COMMENTS FOR POST
@comment_bp.route("/posts/<int:post_id>/comments", methods=["GET"])
def get_comments(post_id):
    post = db.session.get(Post, post_id)
    if not post:
        abort(404)

    comments = Comment.query.filter_by(post_id=post_id).all()

    return success_response({
        "items": [comment.to_dict() for comment in comments],
        "total": len(comments)
    })

# UPDATE COMMENT
@comment_bp.route("/comments/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)

    text = data.get("text")
    if not text or text.strip() == "":
        return error_response("Comment text is required", 400)

    comment = db.session.get(Comment, comment_id)
    if not comment:
        abort(404)

    if comment.user_id != user_id:
        abort(403)

    comment.text = text
    db.session.commit()

    return success_response(
        data=comment.to_dict(),
        message="Comment updated"
    )

# DELETE COMMENT
@comment_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    user_id = int(get_jwt_identity())

    comment = db.session.get(Comment, comment_id)
    if not comment:
        abort(404)

    if comment.user_id != user_id:
        abort(403)

    db.session.delete(comment)
    db.session.commit()

    return success_response(
        message="Comment deleted successfully"
    )