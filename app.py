from flask import Flask
from apptelemetry import get_logger; import os;
from dotenv import load_dotenv

load_dotenv();

# Import blueprints
from routes.main import main_bp
from routes.health import health_bp
from routes.errors import error_bp
from routes.api import bp_api
from routes.posts_route import posts_bp
from utils.context_processors import load_contexts
from routes.dashboard_route import bp_dashboard

# Import middleware
from middleware.request_logging import register_middleware

app = Flask(__name__)
app.secret_key =os.getenv('WTF_CSRF_SECRET_KEY', 'default_secret_key')
logger = get_logger(__name__)

# Register middleware
register_middleware(app)
# Load context processors
load_contexts(app)


#region Database connection
from appconfigs.db_conn import get_db_connection
db = get_db_connection(app);
#enderegion

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(health_bp)
app.register_blueprint(error_bp)
app.register_blueprint(bp_api, url_prefix='/api/v1')
app.register_blueprint(posts_bp, url_prefix='/posts')
app.register_blueprint(bp_dashboard, url_prefix='/dashboard')

#region Run only if the script is executed directly
if __name__ == '__main__':
    is_dev = os.getenv("FLASK_ENV") == 'development';
    logger.info("Starting Flask application", extra={
        'event_name': 'app_startup',
        'debug_mode': is_dev
    })
    app.run(debug= is_dev)
#endregion