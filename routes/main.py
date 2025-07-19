from flask import Blueprint, request, render_template, redirect, url_for
from apptelemetry import get_logger
import time

# Create the main blueprint
main_bp = Blueprint('main', __name__)
logger = get_logger(__name__)

@main_bp.route('/')
def hello():
    title = "Hello from Flask API with Azure Monitor! 🚀"
    response = {
        'event_name': 'request_completed',
        'endpoint': request.path,
        'method': request.method,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'client_ip': request.remote_addr,
        'app_module': str(__name__)
    }

    # Make sure the extra parameters are serializable
    logger.info("Request completed successfully", extra=response)
    return render_template('index.html', msg={'title': title, 'message': response})


@main_bp.route('/form', methods=['POST', 'GET'])
def form():
    """Handle form submission"""
    data = request.form

    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    
    logger.info("Form submitted", extra={
        'event_name': 'form_submission',
        'form_data': data
    })
    return render_template('form.html', msg={'title': 'Form Submission', 'message': data}), 200

@main_bp.route('/dashboard')
def dashboard():
    """Render the dashboard page"""
    return render_template('dashboard.html', msg={'title': 'Dashboard'})
