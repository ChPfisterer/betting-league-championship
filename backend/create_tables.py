#!/usr/bin/env python3
"""
Create all database tables using SQLAlchemy models
"""

import sys
import os

# Add the backend src directory to the path
sys.path.insert(0, '/app/src')

from core.database import engine, Base
from models import *  # Import all models to register them with SQLAlchemy

def create_tables():
    """Create all tables in the database"""
    print("🏗️  Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        print("✅ All tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

if __name__ == "__main__":
    success = create_tables()
    sys.exit(0 if success else 1)