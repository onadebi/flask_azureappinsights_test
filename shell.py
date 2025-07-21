#!/usr/bin/env python
"""
Simple shell script to interact with the Flask app and database
"""

from app import app, db
from models.user import User

def main():
    """Start an interactive shell with app context"""
    with app.app_context():
        print("Flask app shell started!")
        print("Available objects:")
        print("  app - Flask application instance")
        print("  db - SQLAlchemy database instance") 
        print("  User - User model class")
        print("\nExample usage:")
        print("  db.create_all()  # Create database tables")
        print("  user = User(username='test', email='test@example.com')")
        print("  db.session.add(user)")
        print("  db.session.commit()")
        
        # Start interactive Python shell
        import code
        code.interact(local=locals())

if __name__ == '__main__':
    main()
