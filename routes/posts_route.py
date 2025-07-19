from flask import Blueprint
from apptelemetry import get_logger

posts_bp = Blueprint('posts', __name__)
logger = get_logger(__name__)

posts ={
    1: {"title": "First Post", "content": "This is the content of the first post."},
    2: {"title": "Second Post", "content": "This is the content of the second post."},
    3: {"title": "Third Post", "content": "This is the content of the third post."},
    4: {"title": "Fourth Post", "content": "This is the content of the fourth post."},
    5: {"title": "Fifth Post", "content": "This is the content of the fifth post."},
    6: {"title": "Sixth Post", "content": "This is the content of the sixth post."}
}

@posts_bp.route('/', methods=['GET'])
def get_posts():
    """Get all posts"""
    logger.info("Fetching all posts")
    return {"posts": posts}

@posts_bp.route('/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get a specific post by ID"""
    post = posts.get(post_id)
    if not post:
        logger.error(f"Post with ID {post_id} not found")
        return {"post": {},
                "error": "Post not found"}, 404
    logger.info(f"Fetching post with ID {post_id}")
    return {"post": post}, 200