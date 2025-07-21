from flask import Flask, Blueprint, render_template
from apptelemetry import get_logger
from services.user_service import get_users
from models.user import User

bp_dashboard = Blueprint('dashboard', __name__, template_folder='../templates/dashboard')
logger = get_logger(__name__)


@bp_dashboard.route('/')
def dashboard():
    """Render the dashboard page"""
    logger.info("Dashboard route hit - rendering dashboard template", extra={
        'event_name': 'dashboard_access',
        'template': 'dashboard/index.htm'
    })
    return render_template('index.htm', msg={'title': 'Dashboard', 'message': 'Welcome to the Dashboard!'})

@bp_dashboard.route('/users')
def all_users():
    """Render the page with all users"""
    allUsers: list[User] = []
    users = get_users(skip=0, limit=100)
    if users[0]:
        allUsers = users[2]
    logger.info("All users route hit - rendering all users template", extra={
        'event_name': 'all_users_access',
        'user_count': len(allUsers)
    })
    return render_template('users.htm', msg={'title': 'All Users', 'users': allUsers, 'message': users[1]})