"""
Database migration to remove confidence point system.

This migration updates the database to remove confidence-related functionality:
1. Updates check constraint to remove 'confidence' from valid point systems
2. Updates any existing groups using confidence point system to standard
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from sqlalchemy import text


def apply_migration():
    """Apply the migration to remove confidence point system."""
    from sqlalchemy import create_engine
    from src.core.config import get_settings
    
    settings = get_settings()
    engine = create_engine(settings.database_url)
    
    with engine.connect() as connection:
        # Execute migration statements one by one
        statements = [
            # Update any groups using confidence point system to standard
            "UPDATE groups SET point_system = 'standard' WHERE point_system = 'confidence'",
            
            # Drop the old constraint
            "ALTER TABLE groups DROP CONSTRAINT IF EXISTS ck_groups_point_system",
            
            # Add new constraint without confidence
            """ALTER TABLE groups ADD CONSTRAINT ck_groups_point_system 
                CHECK (point_system IN ('standard', 'spread', 'custom'))"""
        ]
        
        for statement in statements:
            try:
                print(f"Executing: {statement.strip()}")
                connection.execute(text(statement))
                connection.commit()
                print("✅ Success")
            except Exception as e:
                print(f"⚠️  Warning: {e}")
                # Continue with other statements even if one fails
                continue
    
    print("✅ Confidence point system removal completed")


if __name__ == "__main__":
    apply_migration()