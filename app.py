from flask import Flask
from apptelemetry import get_logger

# Import blueprints
from routes.main import main_bp
from routes.health import health_bp
from routes.errors import error_bp
from routes.api import bp_api

app = Flask(__name__)
logger = get_logger(__name__)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(health_bp)
app.register_blueprint(error_bp)
app.register_blueprint(bp_api, url_prefix='/api/v1')

#region Run only if the script is executed directly
if __name__ == '__main__':
    logger.info("Starting Flask application", extra={
        'event_name': 'app_startup',
        'debug_mode': True
    })
    app.run(debug=True)
#endregion