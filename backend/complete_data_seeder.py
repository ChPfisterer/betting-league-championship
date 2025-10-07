#!/usr/bin/env python3
"""
Complete data seeding script for the betting championship application.

This script seeds the database with both historical and current data:
1. FIFA World Cup 2022 data (historical)
2. Real Bundesliga 2025/26 data (current season)
"""

import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_seeder(script_name, description):
    """Run a seeding script and handle errors gracefully"""
    try:
        logger.info(f"🌱 {description}...")
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        logger.info(f"✅ {description} completed successfully")
        if result.stdout:
            logger.info(f"Output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ {description} failed: {e}")
        if e.stdout:
            logger.error(f"STDOUT: {e.stdout}")
        if e.stderr:
            logger.error(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"❌ Unexpected error in {description}: {e}")
        return False

def main():
    """Main seeding function"""
    logger.info("🚀 Starting complete database seeding...")
    
    success_count = 0
    total_seeders = 2
    
    # 1. FIFA World Cup 2022 data (historical)
    if run_seeder("FINAL_complete_world_cup_seeder.py", "FIFA World Cup 2022 data seeding"):
        success_count += 1
    
    # 2. Real Bundesliga 2025/26 data (current)
    if run_seeder("real_bundesliga_fetcher.py", "Real Bundesliga 2025/26 data seeding"):
        success_count += 1
    
    # Summary
    logger.info(f"🎯 Seeding complete: {success_count}/{total_seeders} datasets loaded successfully")
    
    if success_count == total_seeders:
        logger.info("✅ All datasets loaded successfully!")
        return 0
    elif success_count > 0:
        logger.warning("⚠️  Some datasets failed to load, but database has partial data")
        return 0  # Don't fail completely if some data loaded
    else:
        logger.error("❌ All data seeding failed - database may be empty")
        return 1

if __name__ == "__main__":
    sys.exit(main())