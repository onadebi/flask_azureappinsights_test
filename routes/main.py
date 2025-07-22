import os
from flask import Blueprint, request, render_template, redirect, url_for
from apptelemetry import get_logger
from models.forms import MyForm
from services.user_service import create_user
from utils.helpers import Helpers
from werkzeug.datastructures import FileStorage

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
    user_registration = MyForm()
    reg_msg= '';
    if request.method == 'POST' and user_registration.validate_on_submit():
        # Process the form data
        username = user_registration.name.data
        email = user_registration.email.data
        profile_picture = (None | FileStorage)
        if request.files:
            profile_picture  = request.files.get('profile_picture')
        new_user = create_user(username=username, email=email, profile_picture=profile_picture)
        if new_user[0]:
            return redirect(url_for('main.success',username=username, email=email, id=new_user[2].id))
            # return redirect(url_for('dashboard.dashboard'))
        else:
            reg_msg = new_user[1]
    
    logger.warning("FailedFormSubmission", extra={
        'event_name': 'Invalid form submission',
        'form_data': user_registration.errors if user_registration else 'No form data'
    })
    return render_template('form.html', msg={'title': 'Add New Entry','form': user_registration, "info": reg_msg}), 200



@main_bp.route('/success')
def success():
    username = request.args.get('username')
    email = request.args.get('email')
    id = request.args.get('id')
    return render_template('success.html', msg={'title': 'Success!', 'username': username, 'email': email, 'id': id})
