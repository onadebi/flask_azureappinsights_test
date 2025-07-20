from flask import Blueprint, request, render_template, redirect, url_for
from apptelemetry import get_logger
from models.forms import HealthDataForm

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
    health_form = HealthDataForm()
    if request.method == 'POST' and health_form.validate_on_submit():
        # Process the form data
        date = health_form.date.data
        exercise = health_form.exercise.data
        sleep = health_form.sleep.data
        meditation = health_form.meditation.data
        blood_pressure = health_form.blood_pressure.data
        logger.info("Form submitted successfully", extra={
            'event_name': 'form_submission',
            'form_data': health_form.data
        })
        return redirect(url_for('dashboard.dashboard'))

    logger.warning("FailedFormSubmission", extra={
        'event_name': 'Invalid form submission',
        'form_data': health_form.errors if health_form else 'No form data'
    })
    return render_template('form.html', msg={'title': 'Add New Entry','form': health_form}), 200
