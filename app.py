from turtle import title
from urllib import response
from flask import Flask, request, render_template
import os;
from apptelemetry import get_logger
import time

app = Flask(__name__)
logger = get_logger(__name__)

@app.route('/')
def hello():
    title = "Hello from Flask API with Azure Monitor! 🚀"
    response = {
        'event_name': 'request_completed',
        'endpoint': request.path,
        'method': request.method,
        'user_agent': request.headers.get('User-Agent', 'Unknown'),
        'client_ip': request.remote_addr,
        'app_module': str(__name__)
    };

    # Make sure the extra parameters are serializable
    logger.info("Request completed successfully", extra=response)
    return render_template('index.html', msg={'title': title, 'message': response})

@app.route('/error')
def test_error():
    """Test endpoint to demonstrate error logging"""
    title = "Error Test"
    response= {
            'event_name': 'test_error',
            'endpoint': '/error',
        };
    try:
        # Intentional error for demonstration
        result = 1 / 0
    except Exception as e:
        response['error_message'] = str(e)
        response['error_type']= type(e).__name__
        title += f" - {response['error_message']}"
        logger.error("Test error occurred", extra=response, exc_info=True)
        
        return render_template('error.html', msg={'title': title, 'message': response}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    title = "Health Check"
    start_time = time.time()
    fileName = os.path.basename(__file__);
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



#region Run only if the script is executed directly
if __name__ == '__main__':
    logger.info("Starting Flask application", extra={
        'event_name': 'app_startup',
        'debug_mode': True
    })
    app.run(debug=True)

#endregion