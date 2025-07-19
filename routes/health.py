from flask import Blueprint, request, render_template
from apptelemetry import get_logger
import time
import os

# Create the health blueprint
health_bp = Blueprint('health', __name__)
logger = get_logger(__name__)

@health_bp.route('/health')
def health_check():
    """Health check endpoint"""
    title = "Health Check"
    start_time = time.time()
    fileName = os.path.basename(__file__)
    current_path = os.path.dirname(os.path.abspath(__file__))
 
    # Simulate some processing
    processing_time = round((time.time() - start_time) * 1000, 2)  # in ms
    response = {
        'event_name': 'health_check',
        'endpoint': request.path,
        'status': 'healthy',
        'timestamp': time.time(),
        'method': request.method,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'client_ip': request.remote_addr,
        'app_module': str(__name__),
        'processing_time_ms': processing_time,
        'response_length': len(title)
    }
    logger.info("Health check requested", extra=response)
    return render_template('health.html', msg={'title': title, 'message': response})
