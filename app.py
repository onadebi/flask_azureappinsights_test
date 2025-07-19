from flask import Flask, request
import os;
from apptelemetry import get_logger
import time

app = Flask(__name__)
logger = get_logger(__name__)

@app.route('/')
def hello():
    # Enhanced logging with more context
    start_time = time.time()

    fileName = os.path.basename(__file__);
    current_path = os.path.dirname(os.path.abspath(__file__))
 
    # Simulate some processing
    response = "Hello from Flask API with Azure Monitor! 🚀"
    
    
    # Log completion with timing
    # Make sure the extra parameters are serializable
    processing_time = round((time.time() - start_time) * 1000, 2)  # in ms
    logger.info("Request completed successfully", extra={
        'event_name': 'request_completed',
        'endpoint': request.path,
        'method': request.method,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'client_ip': request.remote_addr,
        'app_module': str(__name__),
        'processing_time_ms': processing_time,
        'response_length': len(response)
    })
    
    return response

@app.route('/error')
def test_error():
    """Test endpoint to demonstrate error logging"""
    try:
        # Intentional error for demonstration
        result = 1 / 0
    except Exception as e:
        logger.error("Test error occurred", extra={
            'event_name': 'test_error',
            'endpoint': '/error',
            'error_type': type(e).__name__,
            'error_message': str(e)
        }, exc_info=True)
        
        return {"error": "Something went wrong", "message": str(e)}, 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    logger.info("Health check requested", extra={
        'event_name': 'health_check',
        'endpoint': '/health',
        'status': 'healthy'
    })
    
    return {"status": "healthy", "timestamp": time.time()}

# Run only if the script is executed directly
if __name__ == '__main__':
    logger.info("Starting Flask application", extra={
        'event_name': 'app_startup',
        'debug_mode': True
    })
    app.run(debug=True)