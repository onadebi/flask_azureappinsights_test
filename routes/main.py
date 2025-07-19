from flask import Blueprint, request, render_template
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
