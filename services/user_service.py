from models.user import User
from appconfigs.db_conn import db;
from apptelemetry import get_logger


logger = get_logger(__name__)

def create_user(username, email) -> tuple[bool, str, (User | None)]:
    """Create a new user in the database"""
    new_user = User(username=username, email=email)
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