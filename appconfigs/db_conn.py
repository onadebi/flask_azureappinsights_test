from flask_sqlalchemy import SQLAlchemy;
from flask import Flask;
from os import getenv;
from apptelemetry import get_logger;

logger = get_logger(__name__)


def get_db_connection(app: Flask) -> SQLAlchemy:
    """Get a database connection"""
    try:
        app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DB_CONNECTION_STRING', 'sqlite:///app.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)
        print(f'Database connection established with URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')
        return db
    except Exception as e:
        # Log the error
        logger.error(f"Database connection error: {e}")
        # You might want to raise the exception again or handle it differently
        raise