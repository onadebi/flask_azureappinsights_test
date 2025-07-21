from flask_sqlalchemy import SQLAlchemy;
from flask import Flask;
from os import getenv;
from apptelemetry import get_logger;
import logging

logger = get_logger(__name__)

# Create a global db instance
db = SQLAlchemy()

def get_db_connection(app: Flask) -> SQLAlchemy:
    """Initialize the database connection with the Flask app"""
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_CONNECTION_STRING', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        if getenv('FLASK_ENV') == 'development':
            # Enable debug mode in development
            # Enable SQL logging
            app.config['SQLALCHEMY_ECHO'] = True
            
            # Configure SQLAlchemy logging
            logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
        
        db.init_app(app)
        print(f'Database connection established with URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
        return db
    except Exception as e:
        # Log the error
        logger.error(f"Database connection error: {e}")
        # You might want to raise the exception again or handle it differently
        raise