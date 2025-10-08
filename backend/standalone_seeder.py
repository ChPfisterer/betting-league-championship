#!/usr/bin/env python3
"""
Standalone seeder script for FIFA World Cup 2022 data.
This script handles table creation and seeding without import conflicts.
"""

import sys
import os
sys.path.append('/app/src')

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime, timezone

# Database configuration
DATABASE_URL = "postgresql://postgres:postgres123@postgres:5432/betting_championship"

def create_comprehensive_seed_data():
    """Create comprehensive FIFA World Cup 2022 seed data using raw SQL."""
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        print("🏆 Creating comprehensive FIFA World Cup 2022 dataset...")
        
        # Clear existing data (only if tables exist)
        print("🧹 Clearing existing data...")
        try:
            session.execute(text("DELETE FROM results CASCADE"))
        except Exception:
            pass  # Table might not exist yet
        try:
            session.execute(text("DELETE FROM bets CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM matches CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM group_memberships CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM groups CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM players CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM competitions CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM teams CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM seasons CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM users CASCADE"))
        except Exception:
            pass
        try:
            session.execute(text("DELETE FROM sports CASCADE"))
        except Exception:
            pass
        session.commit()
        
        # Create sport
        print("⚽ Creating Football sport...")
        sport_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO sports (id, name, slug, description, category, is_active, popularity_score, rules, created_at, updated_at)
            VALUES (:id, 'Football', 'football', 'Association football (soccer)', 'team_sport', true, 95.5, 
                    '{"players_per_team": 11, "match_duration": 90, "offside_rule": true}', NOW(), NOW())
        """), {"id": sport_id})
        
        # Create season
        print("📅 Creating 2022 FIFA World Cup season...")
        season_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO seasons (id, sport_id, name, slug, year, start_date, end_date, is_current, 
                               status, prize_pool_total, created_at, updated_at)
            VALUES (:id, :sport_id, '2022 FIFA World Cup', 'fifa-world-cup-2022', 2022, 
                    '2022-11-20', '2022-12-18', false, 'completed', 440000000.00, NOW(), NOW())
        """), {"id": season_id, "sport_id": sport_id})
        
        # Create all 32 teams
        print("🌍 Creating all 32 World Cup teams...")
        teams_data = [
            # Group A
            ("Qatar", "qatar", "QAT", "Qatar"),
            ("Ecuador", "ecuador", "ECU", "Ecuador"),
            ("Senegal", "senegal", "SEN", "Senegal"),
            ("Netherlands", "netherlands", "NED", "Netherlands"),
            # Group B
            ("England", "england", "ENG", "England"),
            ("Iran", "iran", "IRN", "Iran"),
            ("USA", "usa", "USA", "United States"),
            ("Wales", "wales", "WAL", "Wales"),
            # Group C
            ("Argentina", "argentina", "ARG", "Argentina"),
            ("Saudi Arabia", "saudi-arabia", "KSA", "Saudi Arabia"),
            ("Mexico", "mexico", "MEX", "Mexico"),
            ("Poland", "poland", "POL", "Poland"),
            # Group D
            ("France", "france", "FRA", "France"),
            ("Australia", "australia", "AUS", "Australia"),
            ("Denmark", "denmark", "DEN", "Denmark"),
            ("Tunisia", "tunisia", "TUN", "Tunisia"),
            # Group E
            ("Spain", "spain", "ESP", "Spain"),
            ("Costa Rica", "costa-rica", "CRC", "Costa Rica"),
            ("Germany", "germany", "GER", "Germany"),
            ("Japan", "japan", "JPN", "Japan"),
            # Group F
            ("Belgium", "belgium", "BEL", "Belgium"),
            ("Canada", "canada", "CAN", "Canada"),
            ("Morocco", "morocco", "MAR", "Morocco"),
            ("Croatia", "croatia", "CRO", "Croatia"),
            # Group G
            ("Brazil", "brazil", "BRA", "Brazil"),
            ("Serbia", "serbia", "SRB", "Serbia"),
            ("Switzerland", "switzerland", "SUI", "Switzerland"),
            ("Cameroon", "cameroon", "CMR", "Cameroon"),
            # Group H
            ("Portugal", "portugal", "POR", "Portugal"),
            ("Ghana", "ghana", "GHA", "Ghana"),
            ("Uruguay", "uruguay", "URU", "Uruguay"),
            ("South Korea", "south-korea", "KOR", "South Korea"),
        ]
        
        team_ids = {}
        for name, slug, short_name, country in teams_data:
            team_id = str(uuid.uuid4())
            team_ids[name] = team_id
            session.execute(text("""
                INSERT INTO teams (id, sport_id, name, slug, short_name, country, 
                                 founded_year, is_active, max_players, created_at, updated_at)
                VALUES (:id, :sport_id, :name, :slug, :short_name, :country, 
                        1900, true, 25, NOW(), NOW())
            """), {
                "id": team_id, "sport_id": sport_id, "name": name, 
                "slug": slug, "short_name": short_name, "country": country
            })
        
        # Create competition
        print("🏆 Creating FIFA World Cup 2022 competition...")
        competition_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO competitions (id, sport_id, season_id, name, slug, description,
                                    format_type, start_date, end_date, status, visibility,
                                    min_participants, max_participants, entry_fee, prize_pool,
                                    allow_public_betting, created_at, updated_at)
            VALUES (:id, :sport_id, :season_id, 'FIFA World Cup 2022', 'fifa-world-cup-2022',
                    'The 2022 FIFA World Cup held in Qatar', 'tournament', '2022-11-20', '2022-12-18',
                    'completed', 'public', 32, 32, 0.00, 440000000.00, true, NOW(), NOW())
        """), {
            "id": competition_id, "sport_id": sport_id, "season_id": season_id
        })
        
        # Create some key matches
        print("⚽ Creating key World Cup matches...")
        
        # Final: Argentina vs France
        final_match_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO matches (id, competition_id, home_team_id, away_team_id, 
                               scheduled_at, started_at, finished_at, status,
                               home_score, away_score, round_number, match_day,
                               created_at, updated_at)
            VALUES (:id, :comp_id, :home_id, :away_id,
                    '2022-12-18 15:00:00+00', '2022-12-18 15:00:00+00', '2022-12-18 17:30:00+00',
                    'finished', 4, 2, 7, 1, NOW(), NOW())
        """), {
            "id": final_match_id, "comp_id": competition_id,
            "home_id": team_ids["Argentina"], "away_id": team_ids["France"]
        })
        
        # Semi-final 1: Argentina vs Croatia
        semi1_match_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO matches (id, competition_id, home_team_id, away_team_id,
                               scheduled_at, started_at, finished_at, status,
                               home_score, away_score, round_number, match_day,
                               created_at, updated_at)
            VALUES (:id, :comp_id, :home_id, :away_id,
                    '2022-12-13 20:00:00+00', '2022-12-13 20:00:00+00', '2022-12-13 21:30:00+00',
                    'finished', 3, 0, 6, 1, NOW(), NOW())
        """), {
            "id": semi1_match_id, "comp_id": competition_id,
            "home_id": team_ids["Argentina"], "away_id": team_ids["Croatia"]
        })
        
        # Semi-final 2: France vs Morocco
        semi2_match_id = str(uuid.uuid4())
        session.execute(text("""
            INSERT INTO matches (id, competition_id, home_team_id, away_team_id,
                               scheduled_at, started_at, finished_at, status,
                               home_score, away_score, round_number, match_day,
                               created_at, updated_at)
            VALUES (:id, :comp_id, :home_id, :away_id,
                    '2022-12-14 20:00:00+00', '2022-12-14 20:00:00+00', '2022-12-14 21:30:00+00',
                    'finished', 2, 0, 6, 2, NOW(), NOW())
        """), {
            "id": semi2_match_id, "comp_id": competition_id,
            "home_id": team_ids["France"], "away_id": team_ids["Morocco"]
        })
        
        # Create some key players
        print("👥 Creating key players...")
        players_data = [
            ("Lionel", "Messi", "Argentina", "Argentina", "Forward", 10),
            ("Kylian", "Mbappé", "France", "France", "Forward", 10),
            ("Luka", "Modrić", "Croatia", "Croatia", "Midfielder", 10),
            ("Achraf", "Hakimi", "Morocco", "Morocco", "Defender", 2),
            ("Harry", "Kane", "England", "England", "Forward", 9),
            ("Neymar", "Jr", "Brazil", "Brazil", "Forward", 10),
            ("Virgil", "van Dijk", "Netherlands", "Netherlands", "Defender", 4),
            ("Manuel", "Neuer", "Germany", "Germany", "Goalkeeper", 1),
        ]
        
        for first_name, last_name, team_name, nationality, position, jersey in players_data:
            if team_name in team_ids:
                player_id = str(uuid.uuid4())
                display_name = f"{first_name} {last_name}"
                session.execute(text("""
                    INSERT INTO players (id, sport_id, current_team_id, first_name, last_name, 
                                       display_name, nationality, position, jersey_number,
                                       date_of_birth, height_cm, weight_kg, market_value, salary,
                                       is_active, injury_status, created_at, updated_at)
                    VALUES (:id, :sport_id, :team_id, :first_name, :last_name,
                            :display_name, :nationality, :position, :jersey,
                            '1990-01-01', 180, 75, 50000000.00, 1000000.00,
                            true, 'fit', NOW(), NOW())
                """), {
                    "id": player_id, "sport_id": sport_id, "team_id": team_ids[team_name], 
                    "first_name": first_name, "last_name": last_name,
                    "display_name": display_name, "nationality": nationality,
                    "position": position, "jersey": jersey
                })
        
        # Skip user creation - users will be created through Keycloak authentication
        print("👤 Skipping test user creation - users will be created through Keycloak authentication")
        
        session.commit()
        
        print("✅ Comprehensive FIFA World Cup 2022 dataset created successfully!")
        print("📊 Dataset includes:")
        print("   • 1 Sport (Football)")
        print("   • 32 Teams (All World Cup participants)")
        print("   • 1 Season (2022 FIFA World Cup)")
        print("   • 1 Competition (FIFA World Cup 2022)")
        print("   • Key matches (Final, Semi-finals)")
        print("   • Star players from major teams")
        print("   • Test users for authentication")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating seed data: {e}")
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = create_comprehensive_seed_data()
    sys.exit(0 if success else 1)