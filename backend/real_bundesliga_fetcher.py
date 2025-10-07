import asyncio
import aiohttp
import ssl
import json
import psycopg2
import uuid
from datetime import datetime, timezone, timezone

API_BASE_URL = "https://api.openligadb.de"
BUNDESLIGA_CODE = "bl1"
SEASON_YEAR = "2025"

def get_db_connection():
    """Get database connection"""
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="betting_championship", 
        user="postgres",
        password="postgres123"
    )

def map_api_status_to_db_status(is_finished: bool) -> str:
    """Map OpenLigaDB status to our database status"""
    return 'finished' if is_finished else 'scheduled'

def insert_into_database(teams, matches):
    """Insert fetched data into the database"""
    print("\n💾 Inserting data into database...")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Create/Get Football Sport
        print("1️⃣  Creating Football sport...")
        sport_id = "550e8400-e29b-41d4-a716-446655440000"  # Fixed UUID for football
        current_time = datetime.now(timezone.utc)
        cursor.execute("""
            INSERT INTO sports (id, name, slug, category, description, is_active, popularity_score, created_at, updated_at) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) 
            ON CONFLICT (slug) DO UPDATE SET
                name = EXCLUDED.name,
                category = EXCLUDED.category,
                description = EXCLUDED.description,
                is_active = EXCLUDED.is_active,
                popularity_score = EXCLUDED.popularity_score,
                updated_at = EXCLUDED.updated_at
            RETURNING id
        """, (sport_id, "Football", "football", "team_sport", "Association Football (Soccer)", True, 100, current_time, current_time))
        
        # Get the actual sport_id (in case of conflict)
        result = cursor.fetchone()
        if result:
            sport_id = result[0]
        else:
            # If no result from RETURNING, get it with a SELECT
            cursor.execute("SELECT id FROM sports WHERE slug = 'football'")
            result = cursor.fetchone()
            if result:
                sport_id = result[0]

        # 2. Create Season
        print("2️⃣  Creating 2025/26 season...")
        season_id = str(uuid.uuid4())
        season_start = "2025-08-23"
        season_end = "2026-05-24"

        cursor.execute("""
            INSERT INTO seasons (id, name, slug, sport_id, year, start_date, end_date, status, is_current, prize_pool_total, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                name = EXCLUDED.name,
                sport_id = EXCLUDED.sport_id,
                start_date = EXCLUDED.start_date,
                end_date = EXCLUDED.end_date,
                status = EXCLUDED.status,
                is_current = EXCLUDED.is_current,
                prize_pool_total = EXCLUDED.prize_pool_total
        """, (
            season_id,
            "2025/26",
            "2025-26-bundesliga",
            sport_id,
            2025,
            season_start,
            season_end,
            "active",
            True,
            0.00,  # prize_pool_total
            current_time,
            current_time
        ))

        # Get the actual season_id (in case of conflict)
        cursor.execute("SELECT id FROM seasons WHERE slug = '2025-26-bundesliga'")
        season_id = cursor.fetchone()[0]

        # 3. Create Competition
        print("3️⃣  Creating Bundesliga competition...")
        competition_id = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO competitions (
                id, name, slug, sport_id, season_id, format_type, 
                start_date, end_date, status, description, 
                min_participants, entry_fee, prize_pool, 
                visibility, allow_public_betting, created_at, updated_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (slug) DO UPDATE SET
                name = EXCLUDED.name,
                format_type = EXCLUDED.format_type,
                start_date = EXCLUDED.start_date,
                end_date = EXCLUDED.end_date,
                description = EXCLUDED.description,
                updated_at = EXCLUDED.updated_at
        """, (
            competition_id,
            "Bundesliga 2025/26",
            "bundesliga-2025-26",
            sport_id,
            season_id,
            "league",  # format_type
            season_start,
            season_end,
            "active",
            "German Bundesliga 2025/26 Season",
            18,  # min_participants (18 teams in Bundesliga)
            0.00,  # entry_fee
            0.00,  # prize_pool
            "public",  # visibility
            True,  # allow_public_betting
            current_time,
            current_time
        ))

        # Get the actual competition_id (in case of conflict)
        cursor.execute("SELECT id FROM competitions WHERE slug = 'bundesliga-2025-26'")
        competition_id = cursor.fetchone()[0]

        # 4. Insert Teams
        print("4️⃣  Inserting teams...")
        team_id_mapping = {}
        
        for team in teams:
            team_db_id = str(uuid.uuid4())
            team_api_id = team['teamId']
            team_id_mapping[team_api_id] = team_db_id
            
            team_name = team.get('teamName', team.get('shortName', 'Unknown Team'))
            short_name = team.get('shortName', team_name[:10])
            
            # Generate slug from team name
            slug = team_name.lower().replace(' ', '-').replace('.', '').replace('ü', 'u').replace('ö', 'o').replace('ä', 'a')
            
            cursor.execute("""
                INSERT INTO teams (id, name, slug, short_name, sport_id, country, logo_url, description, is_active, max_players, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (slug) DO UPDATE SET
                    name = EXCLUDED.name,
                    short_name = EXCLUDED.short_name,
                    logo_url = EXCLUDED.logo_url,
                    description = EXCLUDED.description,
                    updated_at = EXCLUDED.updated_at
            """, (
                team_db_id,
                team_name,
                slug,
                short_name,
                sport_id,
                "Germany",
                team.get('teamIconUrl'),
                f"Bundesliga team: {team_name}",
                True,
                25,  # max_players
                current_time,
                current_time
            ))
            
            print(f"   ✅ {team_name}")

        # Update team_id_mapping with actual IDs from database
        for team in teams:
            team_api_id = team['teamId']
            team_name = team.get('teamName', team.get('shortName', 'Unknown Team'))
            slug = team_name.lower().replace(' ', '-').replace('.', '').replace('ü', 'u').replace('ö', 'o').replace('ä', 'a')
            cursor.execute("SELECT id FROM teams WHERE slug = %s", (slug,))
            result = cursor.fetchone()
            if result:
                team_id_mapping[team_api_id] = result[0]

        # 5. Insert Matches
        print("5️⃣  Inserting matches...")
        match_count = 0
        
        for match in matches:
            match_db_id = str(uuid.uuid4())
            
            # Get team IDs
            home_team_api_id = match['team1']['teamId']
            away_team_api_id = match['team2']['teamId']
            
            home_team_id = team_id_mapping.get(home_team_api_id)
            away_team_id = team_id_mapping.get(away_team_api_id)
            
            if not home_team_id or not away_team_id:
                continue
                
            # Parse match date
            match_date = match.get('matchDateTime')
            if match_date:
                scheduled_at = datetime.fromisoformat(match_date)
                scheduled_at = scheduled_at.replace(tzinfo=timezone.utc)
            else:
                continue
                
            # Determine status
            is_finished = match.get('matchIsFinished', False)
            status = map_api_status_to_db_status(is_finished)
            
            # Get scores
            home_score = None
            away_score = None
            match_results = match.get('matchResults', [])
            if match_results:
                final_result = match_results[-1]
                home_score = final_result.get('pointsTeam1')
                away_score = final_result.get('pointsTeam2')
                
            # Get round number
            round_number = match.get('group', {}).get('groupOrderID', 1)
            
            cursor.execute("""
                INSERT INTO matches (
                    id, competition_id, home_team_id, away_team_id, 
                    scheduled_at, status, home_score, away_score,
                    round_number, venue, created_at, updated_at
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO UPDATE SET
                    scheduled_at = EXCLUDED.scheduled_at,
                    status = EXCLUDED.status,
                    home_score = EXCLUDED.home_score,
                    away_score = EXCLUDED.away_score,
                    round_number = EXCLUDED.round_number,
                    updated_at = EXCLUDED.updated_at
            """, (
                match_db_id,
                competition_id,
                home_team_id,
                away_team_id,
                scheduled_at,
                status,
                home_score,
                away_score,
                round_number,
                None,  # venue (no venue info from API)
                current_time,
                current_time
            ))
            
            match_count += 1
            if match_count % 50 == 0:
                print(f"   📝 Processed {match_count} matches...")

        # Commit all changes
        conn.commit()
        
        print(f"\n🎉 Database insertion complete!")
        print(f"✅ Teams: {len(teams)}")
        print(f"✅ Matches: {match_count}")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Database error: {e}")
        raise
    finally:
        cursor.close()
        conn.close()

async def fetch_data():
    """Fetch teams and matches data from OpenLigaDB API"""
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    connector = aiohttp.TCPConnector(ssl=ssl_context)
    
    async with aiohttp.ClientSession(connector=connector) as session:
        # Fetch teams
        print("🔄 Fetching teams...")
        teams_url = f"{API_BASE_URL}/getavailableteams/{BUNDESLIGA_CODE}/{SEASON_YEAR}"
        async with session.get(teams_url) as response:
            if response.status == 200:
                teams = await response.json()
                print(f"✅ Teams fetched: {len(teams)}")
            else:
                print(f"❌ Teams fetch failed: {response.status}")
                return [], []
        
        # Fetch matches
        print("🔄 Fetching matches...")
        matches_url = f"{API_BASE_URL}/getmatchdata/{BUNDESLIGA_CODE}/{SEASON_YEAR}"
        async with session.get(matches_url) as response:
            if response.status == 200:
                matches = await response.json()
                print(f"✅ Matches fetched: {len(matches)}")
            else:
                print(f"❌ Matches fetch failed: {response.status}")
                return teams, []
                
    return teams, matches

async def main():
    """Main function to fetch data from OpenLigaDB API and insert into database"""
    print("🏈 Fetching Bundesliga 2025/26 data from OpenLigaDB...")
    
    # Fetch data from API
    teams, matches = await fetch_data()
    
    if not teams or not matches:
        print("❌ Failed to fetch data from API")
        return
    
    # Save JSON files for inspection
    with open("bundesliga_teams.json", "w", encoding='utf-8') as f:
        json.dump(teams, f, indent=2, ensure_ascii=False)
    print(f"📁 Teams saved to bundesliga_teams.json ({len(teams)} teams)")
    
    with open("bundesliga_matches.json", "w", encoding='utf-8') as f:
        json.dump(matches, f, indent=2, ensure_ascii=False)
    print(f"📁 Matches saved to bundesliga_matches.json ({len(matches)} matches)")
    
    # Insert data into database
    insert_into_database(teams, matches)
    
    print("\n🎯 Data fetching and database insertion complete!")

if __name__ == "__main__":
    asyncio.run(main())
