from flask import Blueprint, render_template
from apptelemetry import get_logger

# Create the error blueprint
error_bp = Blueprint('error', __name__)
logger = get_logger(__name__)

@error_bp.route('/error')
def test_error():
    """Test endpoint to demonstrate error logging"""
    print(f"Blueprint __name__ in errors.py: {__name__}")
    title = "Error Test"
    response = {
        'event_name': 'test_error',
        'endpoint': '/error',
    }
    try:
        # Intentional error for demonstration
        result = 1 / 0
    except Exception as e:
        response['error_message'] = str(e)
        response['error_type'] = type(e).__name__
        title += f" - {response['error_message']}"
        logger.error("Test error occurred", extra=response, exc_info=True)
        
        return render_template('error.html', msg={'title': title, 'message': response}), 500
