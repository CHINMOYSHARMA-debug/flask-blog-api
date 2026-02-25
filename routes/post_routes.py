from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Post
from extensions import db
from utils.responses import success_response, error_response

post_bp = Blueprint("posts", __name__)

# GET ALL POSTS (Pagination + Search)
@post_bp.route("/posts", methods=["GET"])
def get_posts():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    search = request.args.get("search", "", type=str)

    query = Post.query

    if search:
        query = query.filter(Post.title.ilike(f"%{search}%"))

    pagination = query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    posts = [post.to_dict() for post in pagination.items]

    return success_response(
        message="Posts fetched",
        data={
            "items": posts,
            "pagination": {
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    }
)

# GET MY POSTS
@post_bp.route("/my-posts", methods=["GET"])
@jwt_required()
def get_my_posts():
    user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    search = request.args.get("search", "", type=str)

    query = Post.query.filter_by(author_id=user_id)

    if search:
        query = query.filter(
            Post.title.ilike(f"%{search}%") |
            Post.content.ilike(f"%{search}%")
        )

    pagination = query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    posts = [post.to_dict() for post in pagination.items]

    return success_response({
        "items": posts,
        "pagination": {
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page
        }
    })

# CREATE POST
@post_bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    """
    Create a new post
    ---
    tags:
      - Posts
    security:
      - Bearer: []
    parameters:
      - in: header
        name: Authorization
        required: true
        schema:
          type: string
        description: Bearer access token

      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - title
            - content
          properties:
            title:
              type: string
            content:
              type: string

    responses:
      201:
        description: Post created
      400:
        description: Validation error
      401:
        description: Unauthorized
    """

    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)
    if not data.get("title"):
        return error_response("Title is required", 400)
    if not data.get("content"):
        return error_response("Content is required", 400)

    new_post = Post(
        title=data["title"],
        content=data["content"],
        author_id=user_id
    )

    db.session.add(new_post)
    db.session.commit()

    return success_response(
        message="Post created",
        data={
            "id": new_post.id,
            "title": new_post.title,
            "content": new_post.content,
            "author_id": new_post.author_id
        }
    )

# GET SINGLE POST
@post_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = db.session.get(Post, post_id)

    if not post:
        abort(404)

    return success_response({
        "item": post.to_dict()
    })

# UPDATE POST
@post_bp.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)

    post = db.session.get(Post, post_id)

    if not post:
        abort(404)

    # OWNERSHIP CHECK
    if post.author_id != user_id:
        abort(403)

    if "title" in data:
        post.title = data["title"]

    if "content" in data:
        post.content = data["content"]

    db.session.commit()

    return success_response({
        "message": "Post updated",
        "data": post.to_dict()
    })

# DELETE POST
@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())

    post = db.session.get(Post, post_id)

    if not post:
        abort(404)

    if post.author_id != user_id:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    return success_response({
        "message": "Post deleted"
    })