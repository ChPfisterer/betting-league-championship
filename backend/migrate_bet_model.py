"""
Database migration to align bet model with specification.

This migration transforms the betting system from traditional sports betting
to a simple prediction contest system as specified.
"""

import sys
import os
from pathlib import Path

# Add src directory to Python path
backend_dir = Path(__file__).parent
src_dir = backend_dir / "src"
sys.path.insert(0, str(src_dir))

from sqlalchemy import text

# Migration to align bet model with specification
MIGRATION_SQL = """
-- Add new spec-compliant columns
ALTER TABLE bets ADD COLUMN IF NOT EXISTS group_id UUID;
ALTER TABLE bets ADD COLUMN IF NOT EXISTS predicted_winner VARCHAR(10);
ALTER TABLE bets ADD COLUMN IF NOT EXISTS predicted_home_score INTEGER;
ALTER TABLE bets ADD COLUMN IF NOT EXISTS predicted_away_score INTEGER;
ALTER TABLE bets ADD COLUMN IF NOT EXISTS points_earned INTEGER DEFAULT 0;
ALTER TABLE bets ADD COLUMN IF NOT EXISTS is_processed BOOLEAN DEFAULT FALSE;

-- Add foreign key constraint for group_id
ALTER TABLE bets ADD CONSTRAINT fk_bets_group_id 
    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE;

-- Add check constraints for predictions
ALTER TABLE bets ADD CONSTRAINT ck_bets_predicted_winner 
    CHECK (predicted_winner IN ('HOME', 'AWAY', 'DRAW'));
    
ALTER TABLE bets ADD CONSTRAINT ck_bets_predicted_scores_non_negative 
    CHECK (predicted_home_score >= 0 AND predicted_away_score >= 0);

ALTER TABLE bets ADD CONSTRAINT ck_bets_points_valid 
    CHECK (points_earned IN (0, 1, 3));

-- Create unique constraint as per spec
ALTER TABLE bets ADD CONSTRAINT uq_bets_user_match_group 
    UNIQUE (user_id, match_id, group_id);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS ix_bets_group_id ON bets(group_id);
CREATE INDEX IF NOT EXISTS ix_bets_predicted_winner ON bets(predicted_winner);
CREATE INDEX IF NOT EXISTS ix_bets_points_earned ON bets(points_earned);
CREATE INDEX IF NOT EXISTS ix_bets_is_processed ON bets(is_processed);

-- Note: We'll keep the old columns for now to avoid data loss
-- They can be dropped in a later migration after verification
"""

def apply_migration():
    """Apply the migration to align with specification."""
    from sqlalchemy import create_engine
    from src.core.config import get_settings
    
    settings = get_settings()
    engine = create_engine(settings.database_url)
    
    with engine.connect() as connection:
        # Execute migration statements one by one
        statements = [
            "ALTER TABLE bets ADD COLUMN IF NOT EXISTS group_id UUID",
            "ALTER TABLE bets ADD COLUMN IF NOT EXISTS predicted_winner VARCHAR(10)",
            "ALTER TABLE bets ADD COLUMN IF NOT EXISTS predicted_home_score INTEGER",
            "ALTER TABLE bets ADD COLUMN IF NOT EXISTS predicted_away_score INTEGER",
            "ALTER TABLE bets ADD COLUMN IF NOT EXISTS points_earned INTEGER DEFAULT 0",
            "ALTER TABLE bets ADD COLUMN IF NOT EXISTS is_processed BOOLEAN DEFAULT FALSE",
            """ALTER TABLE bets ADD CONSTRAINT fk_bets_group_id 
                FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE""",
            """ALTER TABLE bets ADD CONSTRAINT ck_bets_predicted_winner 
                CHECK (predicted_winner IN ('HOME', 'AWAY', 'DRAW'))""",
            """ALTER TABLE bets ADD CONSTRAINT ck_bets_predicted_scores_non_negative 
                CHECK (predicted_home_score >= 0 AND predicted_away_score >= 0)""",
            "ALTER TABLE bets ADD CONSTRAINT ck_bets_points_valid CHECK (points_earned IN (0, 1, 3))",
            "ALTER TABLE bets ADD CONSTRAINT uq_bets_user_match_group UNIQUE (user_id, match_id, group_id)",
            "CREATE INDEX IF NOT EXISTS ix_bets_group_id ON bets(group_id)",
            "CREATE INDEX IF NOT EXISTS ix_bets_predicted_winner ON bets(predicted_winner)",
            "CREATE INDEX IF NOT EXISTS ix_bets_points_earned ON bets(points_earned)",
            "CREATE INDEX IF NOT EXISTS ix_bets_is_processed ON bets(is_processed)"
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
    
    print("✅ Database migration completed - Bet model aligned with specification")

if __name__ == "__main__":
    apply_migration()