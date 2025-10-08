#!/usr/bin/env python3
"""
Remove odds system from bet model - migrate to prediction contest
"""

import os
import sys
sys.path.append('/Users/chp/repos/GitHub/betting-league-championship/backend/src')

from sqlalchemy import text
from core.database import get_db

def migrate_bet_table():
    """Remove odds and financial fields, add prediction fields"""
    db = next(get_db())
    
    try:
        print("🔄 Migrating bet table to remove odds system...")
        
        # Add new prediction columns if they don't exist
        print("  📝 Adding prediction score columns...")
        db.execute(text("""
            ALTER TABLE bets 
            ADD COLUMN IF NOT EXISTS predicted_home_score INTEGER,
            ADD COLUMN IF NOT EXISTS predicted_away_score INTEGER,
            ADD COLUMN IF NOT EXISTS points_earned INTEGER DEFAULT 0;
        """))
        
        # Remove financial columns and constraints if they exist
        print("  🗑️  Removing financial columns and constraints...")
        
        # Drop constraints first
        constraints_to_drop = [
            "ck_bets_odds_minimum",
            "ck_bets_potential_payout_minimum", 
            "ck_bets_payout_amount_non_negative",
            "ck_bets_commission_non_negative"
        ]
        
        for constraint in constraints_to_drop:
            try:
                db.execute(text(f"ALTER TABLE bets DROP CONSTRAINT IF EXISTS {constraint};"))
                print(f"    ✅ Dropped constraint: {constraint}")
            except Exception as e:
                print(f"    ⚠️  Could not drop constraint {constraint}: {e}")
        
        # Drop financial columns
        financial_columns = ["odds", "stake_amount", "potential_payout", "payout_amount", "commission"]
        
        for column in financial_columns:
            try:
                db.execute(text(f"ALTER TABLE bets DROP COLUMN IF EXISTS {column};"))
                print(f"    ✅ Dropped column: {column}")
            except Exception as e:
                print(f"    ⚠️  Could not drop column {column}: {e}")
        
        # Add points constraint (try to drop first, then add)
        print("  ✅ Adding points constraint...")
        try:
            db.execute(text("ALTER TABLE bets DROP CONSTRAINT IF EXISTS ck_bets_points_earned_range;"))
        except:
            pass
        
        db.execute(text("""
            ALTER TABLE bets 
            ADD CONSTRAINT ck_bets_points_earned_range 
            CHECK (points_earned >= 0 AND points_earned <= 3);
        """))
        
        db.commit()
        print("✅ Bet table migration completed successfully!")
        
        # Verify changes
        print("\n📊 Verifying table structure...")
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'bets' 
            ORDER BY ordinal_position;
        """))
        
        print("Current bet table columns:")
        for row in result:
            print(f"  - {row.column_name}: {row.data_type} (nullable: {row.is_nullable})")
            
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        db.rollback()
        return False
    
    finally:
        db.close()
    
    return True

if __name__ == "__main__":
    print("🧪 Migrating Bet Model to Remove Odds System")
    print("=" * 50)
    
    success = migrate_bet_table()
    
    print("=" * 50)
    if success:
        print("✅ Migration completed successfully!")
        print("🎯 Betting system transformed to prediction contest!")
        sys.exit(0)
    else:
        print("❌ Migration failed!")
        sys.exit(1)