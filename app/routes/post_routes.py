from flask import Blueprint, request, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Post, db
from app.extensions import db
from app.utils.responses import success_response, error_response
from app.services import post_service

post_bp = Blueprint("posts", __name__)

# GET ALL POSTS (Pagination + Search)
@post_bp.route("/posts", methods=["GET"])
def get_posts():
    
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    search = request.args.get("search", "", type=str)
    sort = request.args.get("sort", "new", type=str)
    
    query = Post.query

    if search: #searching
        query = query.filter(Post.title.ilike(f"%{search}%"))

    if sort == "old":
        query = query.order_by(Post.id.asc())
    else:
        query = query.order_by(Post.created_at.desc())

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    posts = [post.to_dict() for post in pagination.items]
    return success_response(
        message="Posts fetched",
        data={
            "items": posts,
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": pagination.page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev
        }
    )

# GET MY POSTS
@post_bp.route("/my-posts", methods=["GET"])
@jwt_required()
def get_my_posts():
    user_id = get_jwt_identity()

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    search = request.args.get("search", "", type=str)

    posts, pagination = post_service.get_my_posts(page, per_page, search, user_id)

    return success_response({
        "items": [post.to_dict() for post in posts],
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
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        if data is None:
            return error_response("Request body must be JSON", 400)
        if not data.get("title"):
            return error_response("Title is required", 400)
        if not data.get("content"):
            return error_response("Content is required", 400)

        new_post = post_service.create_post(
            user_id,
            data.get("title"),
            data.get("content")
        )

        return success_response(
            message="Post created",
            data={
                "id": new_post.id,
                "title": new_post.title,
                "content": new_post.content,
                "author_id": new_post.author_id,
            },
            status_code=201
        )

    except Exception as e:
        print("ERROR:", e)
        return error_response("Internal error", 500)

# GET SINGLE POST
@post_bp.route("/posts/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get(post_id)

    if not post:
        return error_response("Post not found", 404)

    return success_response(
        message="Post fetched",
        data=post.to_dict()
    )

# UPDATE POST
@post_bp.route("/posts/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if data is None:
        return error_response("Request body must be JSON", 400)
    if not data.get("title") or not data.get("content"):
        return error_response("Title and Content required", 400) 

    post, error = post_service.update_post(post_id, user_id, data)

    if error == "not_found":
        return error_response("Post not found", 404)

    if error == "forbidden":
        return error_response("Unauthorized", 403)

    return success_response(
        message = "Post updated",
        data = post.to_dict()
    )

# DELETE POST
@post_bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    try:
        user_id = int(get_jwt_identity())

        error = post_service.delete_post(post_id, user_id)

        if error == "not_found":
            return error_response("Post not found", 404)

        if error == "forbidden":
            return error_response("Unauthorized", 403)

        return success_response(
            message = "Post deleted",
            data={"post_id" : post_id}    
        )
    except Exception as e:
        print("DELETE ERROR:", e)
        return error_response("Internal server error", 500)
    