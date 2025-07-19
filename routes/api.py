from flask import Blueprint, request
import time
import os
from apptelemetry import get_logger

bp_api = Blueprint('api', __name__)
logger = get_logger(__name__)


@bp_api.route('/health', methods=['GET'])
def api_endpoint():
    """Health check endpoint"""
    title = "Health Check"
    start_time = time.time()
 
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
        'response_length': len(title),
        'file_name': os.path.basename(__file__),
        'current_path': os.path.dirname(os.path.abspath(__file__))
    }
    logger.info("Health check requested", extra=response)
    return response;
