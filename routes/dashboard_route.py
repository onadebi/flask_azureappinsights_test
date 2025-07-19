from flask import Flask, Blueprint, render_template
from apptelemetry import get_logger

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