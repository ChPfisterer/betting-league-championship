#!/usr/bin/env python3
"""
Clean database script to remove all betting data and reset for fresh import.
"""

import psycopg2

def clean_database():
    """Clean all betting-related data from the database"""
    print("🧹 Cleaning database...")
    
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="betting_championship", 
        user="postgres",
        password="postgres123"
    )
    cursor = conn.cursor()
    
    try:
        # Delete in reverse dependency order
        print("1️⃣  Deleting bets...")
        cursor.execute("DELETE FROM bets;")
        
        print("2️⃣  Deleting matches...")
        cursor.execute("DELETE FROM matches;")
        
        print("3️⃣  Deleting players...")
        cursor.execute("DELETE FROM players;")
        
        print("4️⃣  Deleting teams...")
        cursor.execute("DELETE FROM teams;")
        
        print("5️⃣  Deleting competitions...")
        cursor.execute("DELETE FROM competitions;")
        
        print("6️⃣  Deleting seasons...")
        cursor.execute("DELETE FROM seasons;")
        
        print("7️⃣  Deleting sports...")
        cursor.execute("DELETE FROM sports;")
        
        # Commit changes
        conn.commit()
        print("✅ Database cleaned successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Error cleaning database: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    clean_database()