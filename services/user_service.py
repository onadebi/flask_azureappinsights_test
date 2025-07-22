import os
from models.user import User
from appconfigs.db_conn import db;
from apptelemetry import get_logger
from werkzeug.datastructures import FileStorage

from utils.helpers import Helpers


logger = get_logger(__name__)

def create_user(username: str, email: str, profile_picture: (FileStorage | None) = None) -> tuple[bool, str, (User | None)]:
    """Create a new user in the database"""
    if profile_picture:
                profile_picture_url = Helpers.guid() + "_" + profile_picture.filename.strip().replace(' ', '_')
                # create uploads folder if it doesn't exist
                if not os.path.exists(os.path.join('static', 'uploads')):
                    os.makedirs(os.path.join('static', 'uploads'))
                # updated file to static/uploads folder
                profile_picture.save(os.path.join('static', 'uploads', profile_picture_url))
    new_user = User(username=username, email=email, profile_picture=profile_picture_url if profile_picture else None)
    try:
        db.session.add(new_user)
        db.session.commit()
        logger.info("Form submitted successfully", extra={
            'event_name': 'form_submission',
            'form_data': {username: username, 'email': email}
        })
        return (True, str(new_user), new_user)
    except Exception as e:
        db.session.rollback()
        error_msg = f"Error creating user: {e}"
        print(error_msg)
        return (False, error_msg, None)
    

def get_users(skip: int = 0, limit: int = 10) -> tuple[bool, str, list[User]]:
    """Get paginated and skipped users"""
    try:
        users = User.query.offset(skip).limit(limit).all()
        if not users:
            return (False, "No users found", [])
        return (True, "Users retrieved successfully", users)
    except Exception as e:
        error_msg = f"Error retrieving users: {e}"
        logger.error(error_msg)
        return (False, error_msg, [])