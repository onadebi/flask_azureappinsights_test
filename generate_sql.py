#!/usr/bin/env python
"""
Generate SQL scripts from SQLAlchemy models without executing them
"""

from app import app, db
from models.user import User
from sqlalchemy.schema import CreateTable
from sqlalchemy.dialects import postgresql

def generate_sql():
    """Generate and display SQL creation scripts"""
    
    with app.app_context():
        print("=== SQL CREATION SCRIPTS ===\n")
        
        # Get all tables from the metadata
        for table in db.metadata.tables.values():
            # Generate CREATE TABLE statement
            create_table = CreateTable(table)
            
            # Compile to specific dialect (PostgreSQL in your case)
            sql = str(create_table.compile(dialect=postgresql.dialect()))
            
            print(f"-- Table: {table.name}")
            print(sql)
            print("\n" + "="*50 + "\n")

if __name__ == '__main__':
    generate_sql()
