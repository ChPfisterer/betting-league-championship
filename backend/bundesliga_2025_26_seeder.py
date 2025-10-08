#!/usr/bin/env python3
"""
Bundesliga 2025/26 Season Seeder

Creates realistic Bundesliga 2025/26 season data with:
- 18 Bundesliga teams
- Current season matches (August 2025 - May 2026)
- Finished matches (Matchdays 1-8)
- Live matches (October 7, 2025)
- Upcoming matches (October-November 2025)
"""

import sys
import os
sys.path.append('./src')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime, timezone, timedelta

# Use localhost database URL directly (following standalone_seeder.py pattern)
DATABASE_URL = "postgresql://postgres:postgres123@localhost:5432/betting_championship"

def create_bundesliga_2025_26_data():
    """Create Bundesliga 2025/26 season data."""
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("🇩🇪 Creating Bundesliga 2025/26 Season Dataset...")
        print("=" * 60)
        
        # Use existing Football sport
        print("⚽ Getting Football sport...")
        result = session.execute(text("SELECT id FROM sports WHERE name = 'Football'"))
        sport_row = result.fetchone()
        if not sport_row:
            # Create Football sport if it doesn't exist
            sport_id = str(uuid.uuid4())
            session.execute(text("""
                INSERT INTO sports (id, name, slug, description, category, is_active, popularity_score, rules, created_at, updated_at)
                VALUES (:id, 'Football', 'football', 'Association football (soccer)', 'team_sport', true, 95.5, 
                        '{"players_per_team": 11, "match_duration": 90, "offside_rule": true}', NOW(), NOW())
            """), {"id": sport_id})
        else:
            sport_id = sport_row[0]
        
        # Create Bundesliga 2025/26 Season
        print("🏆 Creating Bundesliga 2025/26 season...")
        season_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO seasons (id, sport_id, name, slug, year, start_date, end_date, is_current, 
                               status, prize_pool_total, created_at, updated_at)
            VALUES (:id, :sport_id, 'Bundesliga 2025/26', 'bundesliga-2025-26', 2025, 
                    '2025-08-15', '2026-05-23', true, 'active', 0.00, NOW(), NOW())
        """), {"id": season_id, "sport_id": sport_id})
        
        # Create Bundesliga Competition
        print("🏟️ Creating Bundesliga competition...")
        competition_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO competitions (id, sport_id, season_id, name, slug, description,
                                    format_type, start_date, end_date, status, visibility,
                                    min_participants, max_participants, entry_fee, prize_pool,
                                    allow_public_betting, created_at, updated_at)
            VALUES (:id, :sport_id, :season_id, 'Bundesliga', 'bundesliga-2025-26',
                    'German Bundesliga 2025/26 Season', 'league', '2025-08-15', '2026-05-23',
                    'active', 'public', 18, 18, 0.00, 0.00, true, NOW(), NOW())
        """), {
            "id": competition_id, "sport_id": sport_id, "season_id": season_id
        })
        
        # Create 18 Bundesliga Teams
        print("👥 Creating 18 Bundesliga teams...")
        bundesliga_teams = [
            # Top Teams
            ("Bayern Munich", "Munich", "Germany"),
            ("Borussia Dortmund", "Dortmund", "Germany"), 
            ("RB Leipzig", "Leipzig", "Germany"),
            ("Bayer Leverkusen", "Leverkusen", "Germany"),
            ("Eintracht Frankfurt", "Frankfurt", "Germany"),
            ("VfB Stuttgart", "Stuttgart", "Germany"),
            
            # Mid-table Teams  
            ("Borussia Mönchengladbach", "Mönchengladbach", "Germany"),
            ("Union Berlin", "Berlin", "Germany"),
            ("SC Freiburg", "Freiburg", "Germany"),
            ("TSG Hoffenheim", "Hoffenheim", "Germany"),
            ("VfL Wolfsburg", "Wolfsburg", "Germany"),
            ("Werder Bremen", "Bremen", "Germany"),
            
            # Lower Teams
            ("FC Augsburg", "Augsburg", "Germany"),
            ("1. FSV Mainz 05", "Mainz", "Germany"),
            ("1. FC Heidenheim", "Heidenheim", "Germany"),
            ("VfL Bochum", "Bochum", "Germany"),
            ("SV Darmstadt 98", "Darmstadt", "Germany"),
            ("FC St. Pauli", "Hamburg", "Germany")
        ]
        
        team_ids = {}
        for name, city, country in bundesliga_teams:
            team_id = str(uuid.uuid4())
            team_ids[name] = team_id
            # Create slug from name
            slug = name.lower().replace(" ", "-").replace(".", "").replace("ü", "u").replace("ö", "o")
            short_name = name.replace("FC ", "").replace("1. ", "").replace("TSG ", "").replace("VfL ", "").replace("VfB ", "").replace("SV ", "")[:3].upper()
            
            session.execute(text("""
                INSERT INTO teams (id, sport_id, name, slug, short_name, country, 
                                 founded_year, is_active, max_players, created_at, updated_at)
                VALUES (:id, :sport_id, :name, :slug, :short_name, :country, 
                        1900, true, 25, NOW(), NOW())
            """), {
                "id": team_id, "sport_id": sport_id, "name": name, 
                "slug": slug, "short_name": short_name, "country": country
            })
        
        print(f"✅ Created {len(team_ids)} Bundesliga teams")
        
        # Create matches for different matchdays with realistic scheduling
        print("📅 Creating matches for 2025/26 season...")
        
        # Matchday 1-8: Finished matches (August-September 2025)
        finished_matches = create_finished_matches(session, competition_id, team_ids)
        
        # Live matches (October 7, 2025 - today)
        live_matches = create_live_matches(session, competition_id, team_ids)
        
        # Upcoming matches (October-November 2025) 
        upcoming_matches = create_upcoming_matches(session, competition_id, team_ids)
        
        session.commit()
        
        print("\n" + "=" * 60)
        print("✅ Bundesliga 2025/26 Season Created Successfully!")
        print(f"📊 Summary:")
        print(f"   • Teams: {len(team_ids)}")
        print(f"   • Finished Matches: {finished_matches}")
        print(f"   • Live Matches: {live_matches}")
        print(f"   • Upcoming Matches: {upcoming_matches}")
        print(f"   • Total Matches: {finished_matches + live_matches + upcoming_matches}")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Error creating Bundesliga data: {e}")
        raise
    finally:
        session.close()


def create_finished_matches(session, competition_id, team_ids):
    """Create finished matches from Matchdays 1-8 (August-September 2025)."""
    print("  📋 Creating finished matches (Matchdays 1-8)...")
    
    teams = list(team_ids.keys())
    match_count = 0
    
    # Sample finished matches with realistic results
    finished_fixtures = [
        # Matchday 1 (August 24, 2025)
        ("Bayern Munich", "Werder Bremen", "2025-08-24 15:30:00+00", 3, 0),
        ("Borussia Dortmund", "Eintracht Frankfurt", "2025-08-24 15:30:00+00", 2, 1),
        ("RB Leipzig", "VfL Bochum", "2025-08-24 15:30:00+00", 4, 1),
        ("Bayer Leverkusen", "Borussia Mönchengladbach", "2025-08-24 18:30:00+00", 1, 2),
        
        # Matchday 2 (August 31, 2025)
        ("VfB Stuttgart", "Bayern Munich", "2025-08-31 15:30:00+00", 1, 3),
        ("Eintracht Frankfurt", "TSG Hoffenheim", "2025-08-31 15:30:00+00", 2, 0),
        ("Werder Bremen", "Borussia Dortmund", "2025-08-31 18:30:00+00", 0, 2),
        ("FC Augsburg", "RB Leipzig", "2025-08-31 15:30:00+00", 1, 1),
        
        # Matchday 3 (September 14, 2025)
        ("Bayern Munich", "Bayer Leverkusen", "2025-09-14 15:30:00+00", 2, 2),
        ("Borussia Dortmund", "Union Berlin", "2025-09-14 15:30:00+00", 3, 1),
        ("VfL Wolfsburg", "Eintracht Frankfurt", "2025-09-14 18:30:00+00", 1, 0),
        ("SC Freiburg", "VfB Stuttgart", "2025-09-14 15:30:00+00", 2, 1),
        
        # Add more matches through Matchday 8...
        ("RB Leipzig", "Bayern Munich", "2025-09-28 18:30:00+00", 1, 4),
        ("1. FSV Mainz 05", "Borussia Dortmund", "2025-09-28 15:30:00+00", 0, 3),
        ("TSG Hoffenheim", "Werder Bremen", "2025-09-28 15:30:00+00", 2, 1),
    ]
    
    for home_team, away_team, scheduled_at, home_score, away_score in finished_fixtures:
        if home_team in team_ids and away_team in team_ids:
            match_id = str(uuid.uuid4())
            
            # Calculate finished time (2 hours after start)
            finished_time = datetime.fromisoformat(scheduled_at.replace('+00', '+00:00')) + timedelta(hours=2)
            finished_at_str = finished_time.strftime('%Y-%m-%d %H:%M:%S+00')
            
            session.execute(text("""
                INSERT INTO matches (id, competition_id, home_team_id, away_team_id,
                                   scheduled_at, started_at, finished_at, status,
                                   home_score, away_score, round_number, match_day,
                                   created_at, updated_at)
                VALUES (:id, :comp_id, :home_id, :away_id,
                        :scheduled_at, :scheduled_at, :finished_at,
                        'finished', :home_score, :away_score, 1, 1, 
                        NOW(), NOW())
            """), {
                "id": match_id,
                "comp_id": competition_id,
                "home_id": team_ids[home_team],
                "away_id": team_ids[away_team],
                "scheduled_at": scheduled_at,
                "finished_at": finished_at_str,
                "home_score": home_score,
                "away_score": away_score
            })
            match_count += 1
    
    print(f"    ✅ Created {match_count} finished matches")
    return match_count


def create_live_matches(session, competition_id, team_ids):
    """Create live matches happening right now (October 7, 2025)."""
    print("  🔴 Creating live matches (October 7, 2025)...")
    
    # Matches happening "right now"
    now = datetime(2025, 10, 7, 15, 30, tzinfo=timezone.utc)  # 3:30 PM UTC
    
    live_fixtures = [
        ("Bayern Munich", "Eintracht Frankfurt", 2, 1, 67),  # 67th minute
        ("Borussia Dortmund", "SC Freiburg", 1, 0, 42),     # 42nd minute  
    ]
    
    match_count = 0
    for home_team, away_team, home_score, away_score, minute in live_fixtures:
        if home_team in team_ids and away_team in team_ids:
            match_id = str(uuid.uuid4())
            started_at = now - timedelta(minutes=minute)
            
            session.execute(text("""
                INSERT INTO matches (id, competition_id, home_team_id, away_team_id,
                                   scheduled_at, started_at, finished_at, status,
                                   home_score, away_score, round_number, match_day,
                                   created_at, updated_at)
                VALUES (:id, :comp_id, :home_id, :away_id,
                        :scheduled_at, :started_at, NULL,
                        'live', :home_score, :away_score, 9, 1,
                        NOW(), NOW())
            """), {
                "id": match_id,
                "comp_id": competition_id, 
                "home_id": team_ids[home_team],
                "away_id": team_ids[away_team],
                "scheduled_at": started_at,
                "started_at": started_at,
                "home_score": home_score,
                "away_score": away_score
            })
            match_count += 1
    
    print(f"    ✅ Created {match_count} live matches")
    return match_count


def create_upcoming_matches(session, competition_id, team_ids):
    """Create upcoming matches (October-November 2025)."""
    print("  📅 Creating upcoming matches (October-November 2025)...")
    
    upcoming_fixtures = [
        # This weekend (October 12, 2025)
        ("RB Leipzig", "VfL Wolfsburg", "2025-10-12 15:30:00+00"),
        ("Bayer Leverkusen", "Union Berlin", "2025-10-12 15:30:00+00"),
        ("VfB Stuttgart", "TSG Hoffenheim", "2025-10-12 18:30:00+00"),
        ("1. FSV Mainz 05", "FC Augsburg", "2025-10-13 15:30:00+00"),
        
        # Next weekend (October 19, 2025)
        ("Werder Bremen", "Bayern Munich", "2025-10-19 15:30:00+00"),
        ("Eintracht Frankfurt", "Bayer Leverkusen", "2025-10-19 15:30:00+00"), 
        ("VfL Wolfsburg", "Borussia Dortmund", "2025-10-19 18:30:00+00"),
        ("Union Berlin", "SC Freiburg", "2025-10-20 15:30:00+00"),
        
        # Following weekend (October 26, 2025)
        ("Bayern Munich", "VfL Bochum", "2025-10-26 15:30:00+00"),
        ("Borussia Dortmund", "RB Leipzig", "2025-10-26 18:30:00+00"),
        ("SC Freiburg", "1. FSV Mainz 05", "2025-10-26 15:30:00+00"),
        
        # Early November (November 2, 2025)
        ("TSG Hoffenheim", "Bayern Munich", "2025-11-02 15:30:00+00"),
        ("VfL Bochum", "Eintracht Frankfurt", "2025-11-02 15:30:00+00"),
        ("FC Augsburg", "Borussia Dortmund", "2025-11-03 18:30:00+00"),
    ]
    
    match_count = 0
    for home_team, away_team, scheduled_at in upcoming_fixtures:
        if home_team in team_ids and away_team in team_ids:
            match_id = str(uuid.uuid4())
            
            session.execute(text("""
                INSERT INTO matches (id, competition_id, home_team_id, away_team_id,
                                   scheduled_at, started_at, finished_at, status,
                                   home_score, away_score, round_number, match_day,
                                   created_at, updated_at)
                VALUES (:id, :comp_id, :home_id, :away_id,
                        :scheduled_at, NULL, NULL, 'scheduled',
                        NULL, NULL, 10, 1, NOW(), NOW())
            """), {
                "id": match_id,
                "comp_id": competition_id,
                "home_id": team_ids[home_team], 
                "away_id": team_ids[away_team],
                "scheduled_at": scheduled_at
            })
            match_count += 1
    
    print(f"    ✅ Created {match_count} upcoming matches")
    return match_count


if __name__ == "__main__":
    create_bundesliga_2025_26_data()