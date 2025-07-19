from flask import Flask,request, g, Response
from apptelemetry import get_logger
import time
import json

logger = get_logger(__name__)

def log_request_info() -> None:
    """Middleware to log incoming request details"""
    # Skip logging for automated/system requests
    skip_paths = [
        '/.well-known/',      # Chrome DevTools
        '/favicon.ico',       # Browser icon requests
        '/apple-touch-icon',  # iOS icon requests
        '/robots.txt',        # SEO crawlers
        '/sitemap.xml'        # SEO sitemaps
    ]
    
    # Check if we should skip this request
    should_skip = any(request.path.startswith(path) for path in skip_paths)
    
    # Store skip flag in g for response middleware
    g.skip_logging = should_skip
    
    if should_skip:
        return
        
    # Store request start time for performance tracking
    g.start_time = time.time()
    
    # Get request data
    url = request.url
    method = request.method
    headers = dict(request.headers)
    
    # Get request body data (if any)
    body_data = None
    if request.content_length and request.content_length > 0:
        try:
            # For JSON requests
            if request.is_json:
                body_data = request.get_json()
            # For form data
            elif request.content_type and 'form' in request.content_type:
                body_data = dict(request.form)
            # For raw data (convert to string for logging)
            else:
                body_data = request.get_data(as_text=True)
        except Exception as e:
            body_data = f"<Could not parse body: {str(e)}>"
    
    # Console output
    print(f"\n🔄 INCOMING REQUEST:")
    print(f"   Method: {method}")
    print(f"   Path: {request.path}")  # Show just the path instead of full URL
    print(f"   Full URL: {url}")       # Show full URL for reference
    # print(f"   User-Agent: {headers.get('User-Agent', 'Unknown')}")
    print(f"   Content-Type: {headers.get('Content-Type', 'None')}")
    print(f"   Content-Length: {headers.get('Content-Length', '0')}")
    
    if body_data:
        print(f"   Body Data: {json.dumps(body_data, indent=2) if isinstance(body_data, (dict, list)) else body_data}")
    else:
        print(f"   Body Data: <No body data>")
    
    # Log to Azure Monitor as well
    logger.info("Request intercepted by middleware", extra={
        'event_name': 'request_intercepted',
        'method': method,
        'url': url,
        'user_agent': headers.get('User-Agent', 'Unknown'),
        'content_type': headers.get('Content-Type', 'None'),
        'content_length': headers.get('Content-Length', 0),
        'has_body_data': body_data is not None
    })

def log_response_info(response: Response) -> Response:
    """Middleware to log outgoing response details"""
    # Skip logging if request was skipped
    if getattr(g, 'skip_logging', False):
        return response
        
    # Calculate request processing time
    processing_time = round((time.time() - g.start_time) * 1000, 2) if hasattr(g, 'start_time') else 0
    
    # Make sure we have a valid status code
    status_code = getattr(response, 'status_code', 200)  # Default to 200 if missing
    content_type = getattr(response, 'content_type', 'unknown')
    
    # Console output
    print(f"✅ RESPONSE SENT:")
    print(f"   Status Code: {status_code}")
    print(f"   Content-Type: {content_type}")
    print(f"   Processing Time: {processing_time}ms")
    print(f"   Response Size: {len(response.get_data())} bytes")
    print("─" * 50)
    
    # Log to Azure Monitor
    logger.info("Response sent", extra={
        'event_name': 'response_sent',
        'status_code': status_code,
        'content_type': content_type,
        'processing_time_ms': processing_time,
        'response_size_bytes': len(response.get_data())
    })
    
    return response

def register_middleware(app: Flask):
    """
    Register all middleware functions with the Flask app
    
    Args:
        app: Flask application instance
    """
    app.before_request(log_request_info)
    app.after_request(log_response_info)
    
    print("✅ Middleware registered successfully")
