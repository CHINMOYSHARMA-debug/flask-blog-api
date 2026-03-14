from app.models import Post
from app.extensions import db

# Post_routes.get_posts
def get_posts(page, per_page, search):
    query = Post.query

    if search:
        query = query.filter(Post.title.ilike(F"%{search}%"))
    
    pagination = query.order_by(Post.id.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return pagination.items, pagination

# get_my_posts
def get_my_posts(page, per_page, search, user_id):
    query = Post.query.filter_by(user_id=user_id)

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

    return pagination.items, pagination

# Create_post
def create_post(user_id, title, content):
    new_post = Post(
        title=title,
        content=content,
        author_id=user_id
    )
    db.session.add(new_post)
    db.session.commit()
    return new_post

# Get_single_post
def get_post_by_id(post_id):
    post = Post.query.get(post_id)

    if not post:
        return None
    return post

#Update_Post
def update_post(post_id, user_id, data):
    post = db.session.get(Post, post_id)

    if not post:
        return None, "not_found"

    if post.author_id != user_id:
        return None, "forbidden"

    post.title = data.get("title")

    post.content = data.get("content")

    db.session.commit()

    return post, None

#Delete_post
def delete_post(post_id, user_id):
    post = db.session.get(Post,post_id)

    if not post:
        return "not_found"

    if post.author_id != user_id:
        return "forbidden"

    db.session.delete(post)
    db.session.commit()

    return None
