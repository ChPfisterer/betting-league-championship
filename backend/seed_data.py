"""
Seed data script for the betting league championship application.

This script populates the database with realistic test data from the 2022 FIFA World Cup
including teams, players, matches, users, and sample betting data.
"""

import sys
import os
sys.path.append('/app/src')

import asyncio
from datetime import datetime, timezone, timedelta, timedelta
from decimal import Decimal
import uuid
from typing import List, Dict, Any

# Import database and models
from database import Base, engine, SessionLocal
from models import (
    Sport, Team, Player, Competition, Season, Match, Result,
    User, Group, GroupMembership, Bet, AuditLog
)

# Import enum classes for validation
from src.models.season import SeasonStatus
from src.models.competition import CompetitionStatus, CompetitionFormat, CompetitionVisibility
from src.models.match import MatchStatus
from src.models.result import ResultStatus
from src.models.group_membership import MembershipRole, MembershipStatus
from src.models.player import InjuryStatus
from src.models.user import UserStatus, UserRole, KYCStatus


def validate_enum_value(enum_class, value: str, context: str = "") -> str:
    """Validate that a value exists in the given enum class."""
    valid_values = [e.value for e in enum_class]
    if value not in valid_values:
        raise ValueError(
            f"Invalid enum value '{value}' for {enum_class.__name__} {context}. "
            f"Valid values: {', '.join(valid_values)}"
        )
    return value


class WorldCupSeeder:
    """Seed data for 2022 FIFA World Cup."""
    
    def __init__(self):
        self.db = SessionLocal()
        self.sport_id = None
        self.season_id = None
        self.competition_id = None
        self.teams = {}
        self.users = {}
        self.groups = {}
    
    def clear_existing_data(self):
        """Clear existing seed data to allow fresh seeding."""
        print("🧹 Clearing existing seed data...")
        
        # Delete in reverse dependency order
        self.db.query(Result).delete()
        self.db.query(Bet).delete() 
        self.db.query(Match).delete()
        self.db.query(GroupMembership).delete()
        self.db.query(Group).delete()
        self.db.query(Player).delete()
        self.db.query(Competition).delete()
        self.db.query(Team).delete()
        self.db.query(Season).delete()
        self.db.query(User).delete()
        self.db.query(Sport).delete()
        
        self.db.commit()
        print("✅ Cleared existing data")
    
    def create_sport(self):
        """Create the Football/Soccer sport."""
        # Check if sport already exists
        existing_sport = self.db.query(Sport).filter(Sport.name == "Football").first()
        if existing_sport:
            self.sport_id = existing_sport.id
            print(f"✅ Found existing sport: {existing_sport.name}")
            return
        
        sport = Sport(
            id=uuid.uuid4(),
            name="Football",
            slug="football",
            description="Association football, commonly known as football or soccer",
            category="team_sport",
            rules="Standard FIFA rules with 11 players per team",
            popularity_score=95.5,
            is_active=True,
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(sport)
        self.db.commit()
        self.sport_id = sport.id
        print(f"✅ Created sport: {sport.name}")
    
    def create_season(self):
        """Create the 2022 season."""
        season = Season(
            id=uuid.uuid4(),
            sport_id=self.sport_id,
            name="2022 Season",
            slug="2022-season",
            year=2022,
            start_date=datetime(2022, 11, 20).date(),
            end_date=datetime(2022, 12, 18).date(),
            is_current=False,
            status=validate_enum_value(SeasonStatus, "completed", "for 2022 Season"),
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(season)
        self.db.commit()
        self.season_id = season.id
        print(f"✅ Created season: {season.name}")
    
    def create_teams(self):
        """Create all 32 World Cup teams."""
        teams_data = [
            # Group A
            {"name": "Qatar", "country": "Qatar", "group": "A"},
            {"name": "Ecuador", "country": "Ecuador", "group": "A"},
            {"name": "Senegal", "country": "Senegal", "group": "A"},
            {"name": "Netherlands", "country": "Netherlands", "group": "A"},
            # Group B
            {"name": "England", "country": "England", "group": "B"},
            {"name": "Iran", "country": "Iran", "group": "B"},
            {"name": "USA", "country": "United States", "group": "B"},
            {"name": "Wales", "country": "Wales", "group": "B"},
            # Group C
            {"name": "Argentina", "country": "Argentina", "group": "C"},
            {"name": "Saudi Arabia", "country": "Saudi Arabia", "group": "C"},
            {"name": "Mexico", "country": "Mexico", "group": "C"},
            {"name": "Poland", "country": "Poland", "group": "C"},
            # Group D
            {"name": "France", "country": "France", "group": "D"},
            {"name": "Australia", "country": "Australia", "group": "D"},
            {"name": "Denmark", "country": "Denmark", "group": "D"},
            {"name": "Tunisia", "country": "Tunisia", "group": "D"},
            # Group E
            {"name": "Spain", "country": "Spain", "group": "E"},
            {"name": "Costa Rica", "country": "Costa Rica", "group": "E"},
            {"name": "Germany", "country": "Germany", "group": "E"},
            {"name": "Japan", "country": "Japan", "group": "E"},
            # Group F
            {"name": "Belgium", "country": "Belgium", "group": "F"},
            {"name": "Canada", "country": "Canada", "group": "F"},
            {"name": "Morocco", "country": "Morocco", "group": "F"},
            {"name": "Croatia", "country": "Croatia", "group": "F"},
            # Group G
            {"name": "Brazil", "country": "Brazil", "group": "G"},
            {"name": "Serbia", "country": "Serbia", "group": "G"},
            {"name": "Switzerland", "country": "Switzerland", "group": "G"},
            {"name": "Cameroon", "country": "Cameroon", "group": "G"},
            # Group H
            {"name": "Portugal", "country": "Portugal", "group": "H"},
            {"name": "Ghana", "country": "Ghana", "group": "H"},
            {"name": "Uruguay", "country": "Uruguay", "group": "H"},
            {"name": "South Korea", "country": "South Korea", "group": "H"},
        ]
        
        for team_data in teams_data:
            team = Team(
                id=uuid.uuid4(),
                sport_id=self.sport_id,
                name=team_data["name"],
                slug=team_data["name"].lower().replace(" ", "-"),
                short_name=team_data["name"][:3].upper(),
                country=team_data["country"],
                current_league=f"World Cup Group {team_data['group']}",
                founded_year=1900,  # Default founding year
                is_active=True,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(team)
            self.teams[team_data["name"]] = team
        
        self.db.commit()
        print(f"✅ Created {len(teams_data)} teams")
    
    def create_competition(self):
        """Create the FIFA World Cup 2022 competition."""
        competition = Competition(
            id=uuid.uuid4(),
            sport_id=self.sport_id,
            season_id=self.season_id,
            name="FIFA World Cup 2022",
            slug="fifa-world-cup-2022",
            description="The 2022 FIFA World Cup held in Qatar",
            format_type=validate_enum_value(CompetitionFormat, "knockout", "for FIFA World Cup 2022"),
            start_date=datetime(2022, 11, 20).date(),
            end_date=datetime(2022, 12, 18).date(),
            status=validate_enum_value(CompetitionStatus, "completed", "for FIFA World Cup 2022"),
            visibility=validate_enum_value(CompetitionVisibility, "public", "for FIFA World Cup 2022"),
            min_participants=32,
            max_participants=32,
            entry_fee=Decimal("0.00"),
            prize_pool=Decimal("440000000.00"),  # $440M total prize money
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc)
        )
        self.db.add(competition)
        self.db.commit()
        self.competition_id = competition.id
        print(f"✅ Created competition: {competition.name}")
    
    def create_key_players(self):
        """Create comprehensive player data for all World Cup teams."""
        players_data = [
            # Group A - Qatar
            {"name": "Almoez Ali", "team": "Qatar", "position": "Forward", "jersey": 19},
            {"name": "Hassan Al-Haydos", "team": "Qatar", "position": "Midfielder", "jersey": 10},
            {"name": "Saad Al Sheeb", "team": "Qatar", "position": "Goalkeeper", "jersey": 22},
            
            # Group A - Ecuador
            {"name": "Enner Valencia", "team": "Ecuador", "position": "Forward", "jersey": 13},
            {"name": "Gonzalo Plata", "team": "Ecuador", "position": "Forward", "jersey": 19},
            {"name": "Hernán Galíndez", "team": "Ecuador", "position": "Goalkeeper", "jersey": 1},
            
            # Group A - Senegal
            {"name": "Sadio Mané", "team": "Senegal", "position": "Forward", "jersey": 10},
            {"name": "Kalidou Koulibaly", "team": "Senegal", "position": "Defender", "jersey": 3},
            {"name": "Édouard Mendy", "team": "Senegal", "position": "Goalkeeper", "jersey": 16},
            
            # Group A - Netherlands
            {"name": "Virgil van Dijk", "team": "Netherlands", "position": "Defender", "jersey": 4},
            {"name": "Memphis Depay", "team": "Netherlands", "position": "Forward", "jersey": 10},
            {"name": "Andries Noppert", "team": "Netherlands", "position": "Goalkeeper", "jersey": 23},
            {"name": "Frenkie de Jong", "team": "Netherlands", "position": "Midfielder", "jersey": 21},
            
            # Group B - England
            {"name": "Harry Kane", "team": "England", "position": "Forward", "jersey": 9},
            {"name": "Jude Bellingham", "team": "England", "position": "Midfielder", "jersey": 22},
            {"name": "Jordan Pickford", "team": "England", "position": "Goalkeeper", "jersey": 1},
            {"name": "Bukayo Saka", "team": "England", "position": "Forward", "jersey": 17},
            {"name": "Declan Rice", "team": "England", "position": "Midfielder", "jersey": 4},
            
            # Group B - Iran
            {"name": "Mehdi Taremi", "team": "Iran", "position": "Forward", "jersey": 9},
            {"name": "Sardar Azmoun", "team": "Iran", "position": "Forward", "jersey": 20},
            {"name": "Alireza Beiranvand", "team": "Iran", "position": "Goalkeeper", "jersey": 1},
            
            # Group B - USA
            {"name": "Christian Pulisic", "team": "USA", "position": "Forward", "jersey": 10},
            {"name": "Tyler Adams", "team": "USA", "position": "Midfielder", "jersey": 4},
            {"name": "Matt Turner", "team": "USA", "position": "Goalkeeper", "jersey": 1},
            {"name": "Yunus Musah", "team": "USA", "position": "Midfielder", "jersey": 8},
            
            # Group B - Wales
            {"name": "Gareth Bale", "team": "Wales", "position": "Forward", "jersey": 11},
            {"name": "Aaron Ramsey", "team": "Wales", "position": "Midfielder", "jersey": 16},
            {"name": "Wayne Hennessey", "team": "Wales", "position": "Goalkeeper", "jersey": 12},
            
            # Group C - Argentina
            {"name": "Lionel Messi", "team": "Argentina", "position": "Forward", "jersey": 10},
            {"name": "Ángel Di María", "team": "Argentina", "position": "Midfielder", "jersey": 11},
            {"name": "Emiliano Martínez", "team": "Argentina", "position": "Goalkeeper", "jersey": 23},
            {"name": "Julián Álvarez", "team": "Argentina", "position": "Forward", "jersey": 9},
            {"name": "Rodrigo De Paul", "team": "Argentina", "position": "Midfielder", "jersey": 7},
            
            # Group C - Saudi Arabia
            {"name": "Salem Al-Dawsari", "team": "Saudi Arabia", "position": "Forward", "jersey": 10},
            {"name": "Saleh Al-Shehri", "team": "Saudi Arabia", "position": "Forward", "jersey": 11},
            {"name": "Mohammed Al-Owais", "team": "Saudi Arabia", "position": "Goalkeeper", "jersey": 21},
            
            # Group C - Mexico
            {"name": "Hirving Lozano", "team": "Mexico", "position": "Forward", "jersey": 22},
            {"name": "Raúl Jiménez", "team": "Mexico", "position": "Forward", "jersey": 9},
            {"name": "Guillermo Ochoa", "team": "Mexico", "position": "Goalkeeper", "jersey": 13},
            
            # Group C - Poland
            {"name": "Robert Lewandowski", "team": "Poland", "position": "Forward", "jersey": 9},
            {"name": "Piotr Zieliński", "team": "Poland", "position": "Midfielder", "jersey": 20},
            {"name": "Wojciech Szczęsny", "team": "Poland", "position": "Goalkeeper", "jersey": 1},
            
            # Group D - France
            {"name": "Kylian Mbappé", "team": "France", "position": "Forward", "jersey": 10},
            {"name": "Antoine Griezmann", "team": "France", "position": "Forward", "jersey": 7},
            {"name": "Hugo Lloris", "team": "France", "position": "Goalkeeper", "jersey": 1},
            {"name": "Olivier Giroud", "team": "France", "position": "Forward", "jersey": 9},
            {"name": "Adrien Rabiot", "team": "France", "position": "Midfielder", "jersey": 14},
            
            # Group D - Australia
            {"name": "Mathew Leckie", "team": "Australia", "position": "Forward", "jersey": 7},
            {"name": "Aaron Mooy", "team": "Australia", "position": "Midfielder", "jersey": 13},
            {"name": "Mathew Ryan", "team": "Australia", "position": "Goalkeeper", "jersey": 1},
            
            # Group D - Denmark
            {"name": "Kasper Dolberg", "team": "Denmark", "position": "Forward", "jersey": 12},
            {"name": "Christian Eriksen", "team": "Denmark", "position": "Midfielder", "jersey": 10},
            {"name": "Kasper Schmeichel", "team": "Denmark", "position": "Goalkeeper", "jersey": 1},
            
            # Group D - Tunisia
            {"name": "Wahbi Khazri", "team": "Tunisia", "position": "Forward", "jersey": 10},
            {"name": "Youssef Msakni", "team": "Tunisia", "position": "Forward", "jersey": 7},
            {"name": "Aymen Dahmen", "team": "Tunisia", "position": "Goalkeeper", "jersey": 26},
            
            # Group E - Spain
            {"name": "Pedri", "team": "Spain", "position": "Midfielder", "jersey": 9},
            {"name": "Gavi", "team": "Spain", "position": "Midfielder", "jersey": 30},
            {"name": "Unai Simón", "team": "Spain", "position": "Goalkeeper", "jersey": 23},
            {"name": "Ferran Torres", "team": "Spain", "position": "Forward", "jersey": 11},
            {"name": "Sergio Busquets", "team": "Spain", "position": "Midfielder", "jersey": 5},
            
            # Group E - Costa Rica
            {"name": "Joel Campbell", "team": "Costa Rica", "position": "Forward", "jersey": 12},
            {"name": "Celso Borges", "team": "Costa Rica", "position": "Midfielder", "jersey": 5},
            {"name": "Keylor Navas", "team": "Costa Rica", "position": "Goalkeeper", "jersey": 1},
            
            # Group E - Germany
            {"name": "Thomas Müller", "team": "Germany", "position": "Forward", "jersey": 25},
            {"name": "Joshua Kimmich", "team": "Germany", "position": "Midfielder", "jersey": 6},
            {"name": "Manuel Neuer", "team": "Germany", "position": "Goalkeeper", "jersey": 1},
            {"name": "Jamal Musiala", "team": "Germany", "position": "Midfielder", "jersey": 42},
            
            # Group E - Japan
            {"name": "Takuma Asano", "team": "Japan", "position": "Forward", "jersey": 18},
            {"name": "Ritsu Doan", "team": "Japan", "position": "Midfielder", "jersey": 8},
            {"name": "Shuichi Gonda", "team": "Japan", "position": "Goalkeeper", "jersey": 12},
            {"name": "Junya Ito", "team": "Japan", "position": "Forward", "jersey": 14},
            
            # Group F - Belgium
            {"name": "Kevin De Bruyne", "team": "Belgium", "position": "Midfielder", "jersey": 7},
            {"name": "Romelu Lukaku", "team": "Belgium", "position": "Forward", "jersey": 9},
            {"name": "Thibaut Courtois", "team": "Belgium", "position": "Goalkeeper", "jersey": 1},
            {"name": "Eden Hazard", "team": "Belgium", "position": "Forward", "jersey": 10},
            
            # Group F - Canada
            {"name": "Alphonso Davies", "team": "Canada", "position": "Defender", "jersey": 19},
            {"name": "Jonathan David", "team": "Canada", "position": "Forward", "jersey": 20},
            {"name": "Milan Borjan", "team": "Canada", "position": "Goalkeeper", "jersey": 18},
            
            # Group F - Morocco
            {"name": "Hakim Ziyech", "team": "Morocco", "position": "Forward", "jersey": 7},
            {"name": "Achraf Hakimi", "team": "Morocco", "position": "Defender", "jersey": 2},
            {"name": "Yassine Bounou", "team": "Morocco", "position": "Goalkeeper", "jersey": 12},
            {"name": "Sofyan Amrabat", "team": "Morocco", "position": "Midfielder", "jersey": 4},
            
            # Group F - Croatia
            {"name": "Luka Modrić", "team": "Croatia", "position": "Midfielder", "jersey": 10},
            {"name": "Ivan Perišić", "team": "Croatia", "position": "Forward", "jersey": 4},
            {"name": "Dominik Livaković", "team": "Croatia", "position": "Goalkeeper", "jersey": 1},
            {"name": "Mateo Kovačić", "team": "Croatia", "position": "Midfielder", "jersey": 8},
            
            # Group G - Brazil
            {"name": "Neymar Jr", "team": "Brazil", "position": "Forward", "jersey": 10},
            {"name": "Casemiro", "team": "Brazil", "position": "Midfielder", "jersey": 5},
            {"name": "Alisson", "team": "Brazil", "position": "Goalkeeper", "jersey": 1},
            {"name": "Vinícius Jr", "team": "Brazil", "position": "Forward", "jersey": 20},
            {"name": "Thiago Silva", "team": "Brazil", "position": "Defender", "jersey": 3},
            
            # Group G - Serbia
            {"name": "Dušan Vlahović", "team": "Serbia", "position": "Forward", "jersey": 9},
            {"name": "Sergej Milinković-Savić", "team": "Serbia", "position": "Midfielder", "jersey": 20},
            {"name": "Vanja Milinković-Savić", "team": "Serbia", "position": "Goalkeeper", "jersey": 23},
            
            # Group G - Switzerland
            {"name": "Granit Xhaka", "team": "Switzerland", "position": "Midfielder", "jersey": 10},
            {"name": "Breel Embolo", "team": "Switzerland", "position": "Forward", "jersey": 7},
            {"name": "Yann Sommer", "team": "Switzerland", "position": "Goalkeeper", "jersey": 1},
            
            # Group G - Cameroon
            {"name": "Vincent Aboubakar", "team": "Cameroon", "position": "Forward", "jersey": 10},
            {"name": "André-Frank Zambo Anguissa", "team": "Cameroon", "position": "Midfielder", "jersey": 8},
            {"name": "André Onana", "team": "Cameroon", "position": "Goalkeeper", "jersey": 24},
            
            # Group H - Portugal
            {"name": "Cristiano Ronaldo", "team": "Portugal", "position": "Forward", "jersey": 7},
            {"name": "Bruno Fernandes", "team": "Portugal", "position": "Midfielder", "jersey": 8},
            {"name": "Diogo Costa", "team": "Portugal", "position": "Goalkeeper", "jersey": 22},
            {"name": "Bernardo Silva", "team": "Portugal", "position": "Midfielder", "jersey": 10},
            
            # Group H - Ghana
            {"name": "André Ayew", "team": "Ghana", "position": "Forward", "jersey": 9},
            {"name": "Thomas Partey", "team": "Ghana", "position": "Midfielder", "jersey": 5},
            {"name": "Lawrence Ati-Zigi", "team": "Ghana", "position": "Goalkeeper", "jersey": 16},
            
            # Group H - Uruguay
            {"name": "Luis Suárez", "team": "Uruguay", "position": "Forward", "jersey": 9},
            {"name": "Federico Valverde", "team": "Uruguay", "position": "Midfielder", "jersey": 15},
            {"name": "Sergio Rochet", "team": "Uruguay", "position": "Goalkeeper", "jersey": 1},
            {"name": "Darwin Núñez", "team": "Uruguay", "position": "Forward", "jersey": 11},
            
            # Group H - South Korea
            {"name": "Son Heung-min", "team": "South Korea", "position": "Forward", "jersey": 7},
            {"name": "Lee Kang-in", "team": "South Korea", "position": "Midfielder", "jersey": 18},
            {"name": "Kim Seung-gyu", "team": "South Korea", "position": "Goalkeeper", "jersey": 21},
        ]
        
        for player_data in players_data:
            if player_data["team"] not in self.teams:
                continue  # Skip if team not found
                
            team = self.teams[player_data["team"]]
            names = player_data["name"].split(" ")
            first_name = names[0]
            last_name = " ".join(names[1:]) if len(names) > 1 else names[0]
            
            player = Player(
                id=uuid.uuid4(),
                sport_id=self.sport_id,
                first_name=first_name,
                last_name=last_name,
                display_name=player_data["name"],
                position=player_data["position"],
                jersey_number=player_data["jersey"],
                date_of_birth=datetime(1995, 1, 1).date(),  # Default birth date
                nationality=team.country,
                current_team_id=team.id,
                market_value=Decimal("50000000.00"),  # $50M default
                salary=Decimal("10000000.00"),  # $10M default
                is_active=True,
                injury_status=validate_enum_value(InjuryStatus, "fit", f"for player {player_data['name']}"),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(player)
        
        self.db.commit()
        print(f"✅ Created {len(players_data)} players from all teams")
    
    def create_sample_users(self):
        """Create sample users for testing."""
        users_data = [
            {
                "username": "admin_user",
                "email": "admin@bettingplatform.com",
                "first_name": "Admin",
                "last_name": "User",
                "role": "admin",
                "status": "active"
            },
            {
                "username": "john_doe",
                "email": "john.doe@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "role": "user",
                "status": "active"
            },
            {
                "username": "jane_smith",
                "email": "jane.smith@example.com",
                "first_name": "Jane",
                "last_name": "Smith",
                "role": "user",
                "status": "active"
            },
            {
                "username": "moderator_mike",
                "email": "mike@bettingplatform.com",
                "first_name": "Mike",
                "last_name": "Wilson",
                "role": "moderator",
                "status": "active"
            },
            {
                "username": "test_user",
                "email": "test@example.com",
                "first_name": "Test",
                "last_name": "User",
                "role": "user",
                "status": "pending"
            }
        ]
        
        for user_data in users_data:
            user = User(
                id=uuid.uuid4(),
                username=user_data["username"],
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                display_name=f"{user_data['first_name']} {user_data['last_name']}",
                date_of_birth=datetime(1990, 1, 1, tzinfo=timezone.utc),  # Default birth date
                password_hash="$2b$12$dummy.hash.for.development.testing.only",  # Dummy hash
                role=user_data["role"],
                status=user_data["status"],
                kyc_status="verified" if user_data["status"] == "active" else "not_started",
                email_verified=True if user_data["status"] == "active" else False,
                phone_verified=False,
                terms_accepted=True,
                privacy_policy_accepted=True,
                marketing_consent=False,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(user)
            self.users[user_data["username"]] = user
        
        self.db.commit()
        print(f"✅ Created {len(users_data)} sample users")
    
    def create_sample_groups(self):
        """Create diverse betting groups for World Cup betting scenarios."""
        groups_data = [
            {
                "name": "World Cup Champions",
                "description": "Elite betting group for World Cup matches",
                "creator": "admin_user",
                "is_private": False
            },
            {
                "name": "Group Stage Experts",
                "description": "Focus on group stage upsets and surprises",
                "creator": "john_doe",
                "is_private": False
            },
            {
                "name": "Knockout Stage Kings",
                "description": "Specialized in elimination rounds and finals",
                "creator": "moderator_mike",
                "is_private": True
            },
            {
                "name": "Underdog Hunters",
                "description": "Betting on upsets and surprise results",
                "creator": "jane_smith",
                "is_private": False
            },
            {
                "name": "Goals and Scores",
                "description": "Focus on over/under and exact score betting",
                "creator": "test_user",
                "is_private": True
            }
        ]
        
        for group_data in groups_data:
            creator = self.users[group_data["creator"]]
            group = Group(
                id=uuid.uuid4(),
                name=group_data["name"],
                description=group_data["description"],
                creator_id=creator.id,
                is_private=group_data["is_private"],
                join_code=f"JOIN{uuid.uuid4().hex[:6].upper()}" if group_data["is_private"] else None,
                max_members=100,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(group)
            self.groups[group_data["name"]] = group
            
            # Add creator as admin member
            membership = GroupMembership(
                id=uuid.uuid4(),
                user_id=creator.id,
                group_id=group.id,
                role=validate_enum_value(MembershipRole, "admin", f"for group {group_data['name']}"),
                status=validate_enum_value(MembershipStatus, "active", f"for group {group_data['name']}"),
                joined_at=datetime.now(timezone.utc),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(membership)
        
        self.db.commit()
        print(f"✅ Created {len(groups_data)} betting groups")
    
    def create_key_matches(self):
        """Create all 64 World Cup 2022 matches with complete results."""
        matches_data = [
            # GROUP STAGE - Group A
            {"home": "Qatar", "away": "Ecuador", "date": "2022-11-20 16:00", "stage": "Group Stage", "home_score": 0, "away_score": 2},
            {"home": "Senegal", "away": "Netherlands", "date": "2022-11-21 16:00", "stage": "Group Stage", "home_score": 0, "away_score": 2},
            {"home": "Qatar", "away": "Senegal", "date": "2022-11-25 13:00", "stage": "Group Stage", "home_score": 1, "away_score": 3},
            {"home": "Netherlands", "away": "Ecuador", "date": "2022-11-25 16:00", "stage": "Group Stage", "home_score": 1, "away_score": 1},
            {"home": "Ecuador", "away": "Senegal", "date": "2022-11-29 15:00", "stage": "Group Stage", "home_score": 1, "away_score": 2},
            {"home": "Netherlands", "away": "Qatar", "date": "2022-11-29 15:00", "stage": "Group Stage", "home_score": 2, "away_score": 0},
            
            # GROUP STAGE - Group B
            {"home": "England", "away": "Iran", "date": "2022-11-21 13:00", "stage": "Group Stage", "home_score": 6, "away_score": 2},
            {"home": "USA", "away": "Wales", "date": "2022-11-21 19:00", "stage": "Group Stage", "home_score": 1, "away_score": 1},
            {"home": "Wales", "away": "Iran", "date": "2022-11-25 10:00", "stage": "Group Stage", "home_score": 0, "away_score": 2},
            {"home": "England", "away": "USA", "date": "2022-11-25 19:00", "stage": "Group Stage", "home_score": 0, "away_score": 0},
            {"home": "Wales", "away": "England", "date": "2022-11-29 19:00", "stage": "Group Stage", "home_score": 0, "away_score": 3},
            {"home": "Iran", "away": "USA", "date": "2022-11-29 19:00", "stage": "Group Stage", "home_score": 0, "away_score": 1},
            
            # GROUP STAGE - Group C
            {"home": "Argentina", "away": "Saudi Arabia", "date": "2022-11-22 10:00", "stage": "Group Stage", "home_score": 1, "away_score": 2},
            {"home": "Mexico", "away": "Poland", "date": "2022-11-22 16:00", "stage": "Group Stage", "home_score": 0, "away_score": 0},
            {"home": "Poland", "away": "Saudi Arabia", "date": "2022-11-26 13:00", "stage": "Group Stage", "home_score": 2, "away_score": 0},
            {"home": "Argentina", "away": "Mexico", "date": "2022-11-26 19:00", "stage": "Group Stage", "home_score": 2, "away_score": 0},
            {"home": "Poland", "away": "Argentina", "date": "2022-11-30 19:00", "stage": "Group Stage", "home_score": 0, "away_score": 2},
            {"home": "Saudi Arabia", "away": "Mexico", "date": "2022-11-30 19:00", "stage": "Group Stage", "home_score": 1, "away_score": 2},
            
            # GROUP STAGE - Group D
            {"home": "Denmark", "away": "Tunisia", "date": "2022-11-22 13:00", "stage": "Group Stage", "home_score": 0, "away_score": 0},
            {"home": "France", "away": "Australia", "date": "2022-11-22 19:00", "stage": "Group Stage", "home_score": 4, "away_score": 1},
            {"home": "Tunisia", "away": "Australia", "date": "2022-11-26 10:00", "stage": "Group Stage", "home_score": 0, "away_score": 1},
            {"home": "France", "away": "Denmark", "date": "2022-11-26 16:00", "stage": "Group Stage", "home_score": 2, "away_score": 1},
            {"home": "Australia", "away": "Denmark", "date": "2022-11-30 15:00", "stage": "Group Stage", "home_score": 1, "away_score": 0},
            {"home": "Tunisia", "away": "France", "date": "2022-11-30 15:00", "stage": "Group Stage", "home_score": 1, "away_score": 0},
            
            # GROUP STAGE - Group E
            {"home": "Germany", "away": "Japan", "date": "2022-11-23 13:00", "stage": "Group Stage", "home_score": 1, "away_score": 2},
            {"home": "Spain", "away": "Costa Rica", "date": "2022-11-23 16:00", "stage": "Group Stage", "home_score": 7, "away_score": 0},
            {"home": "Japan", "away": "Costa Rica", "date": "2022-11-27 10:00", "stage": "Group Stage", "home_score": 0, "away_score": 1},
            {"home": "Spain", "away": "Germany", "date": "2022-11-27 19:00", "stage": "Group Stage", "home_score": 1, "away_score": 1},
            {"home": "Japan", "away": "Spain", "date": "2022-12-01 19:00", "stage": "Group Stage", "home_score": 2, "away_score": 1},
            {"home": "Costa Rica", "away": "Germany", "date": "2022-12-01 19:00", "stage": "Group Stage", "home_score": 2, "away_score": 4},
            
            # GROUP STAGE - Group F
            {"home": "Morocco", "away": "Croatia", "date": "2022-11-23 10:00", "stage": "Group Stage", "home_score": 0, "away_score": 0},
            {"home": "Belgium", "away": "Canada", "date": "2022-11-23 19:00", "stage": "Group Stage", "home_score": 1, "away_score": 0},
            {"home": "Belgium", "away": "Morocco", "date": "2022-11-27 13:00", "stage": "Group Stage", "home_score": 0, "away_score": 2},
            {"home": "Croatia", "away": "Canada", "date": "2022-11-27 16:00", "stage": "Group Stage", "home_score": 4, "away_score": 1},
            {"home": "Croatia", "away": "Belgium", "date": "2022-12-01 15:00", "stage": "Group Stage", "home_score": 0, "away_score": 0},
            {"home": "Canada", "away": "Morocco", "date": "2022-12-01 15:00", "stage": "Group Stage", "home_score": 1, "away_score": 2},
            
            # GROUP STAGE - Group G
            {"home": "Switzerland", "away": "Cameroon", "date": "2022-11-24 10:00", "stage": "Group Stage", "home_score": 1, "away_score": 0},
            {"home": "Brazil", "away": "Serbia", "date": "2022-11-24 19:00", "stage": "Group Stage", "home_score": 2, "away_score": 0},
            {"home": "Cameroon", "away": "Serbia", "date": "2022-11-28 10:00", "stage": "Group Stage", "home_score": 3, "away_score": 3},
            {"home": "Brazil", "away": "Switzerland", "date": "2022-11-28 16:00", "stage": "Group Stage", "home_score": 1, "away_score": 0},
            {"home": "Serbia", "away": "Switzerland", "date": "2022-12-02 19:00", "stage": "Group Stage", "home_score": 2, "away_score": 3},
            {"home": "Cameroon", "away": "Brazil", "date": "2022-12-02 19:00", "stage": "Group Stage", "home_score": 1, "away_score": 0},
            
            # GROUP STAGE - Group H
            {"home": "Uruguay", "away": "South Korea", "date": "2022-11-24 13:00", "stage": "Group Stage", "home_score": 0, "away_score": 0},
            {"home": "Portugal", "away": "Ghana", "date": "2022-11-24 16:00", "stage": "Group Stage", "home_score": 3, "away_score": 2},
            {"home": "South Korea", "away": "Ghana", "date": "2022-11-28 13:00", "stage": "Group Stage", "home_score": 2, "away_score": 3},
            {"home": "Portugal", "away": "Uruguay", "date": "2022-11-28 19:00", "stage": "Group Stage", "home_score": 2, "away_score": 0},
            {"home": "Ghana", "away": "Uruguay", "date": "2022-12-02 15:00", "stage": "Group Stage", "home_score": 0, "away_score": 2},
            {"home": "South Korea", "away": "Portugal", "date": "2022-12-02 15:00", "stage": "Group Stage", "home_score": 2, "away_score": 1},
            
            # ROUND OF 16
            {"home": "Netherlands", "away": "USA", "date": "2022-12-03 15:00", "stage": "Round of 16", "home_score": 3, "away_score": 1},
            {"home": "Argentina", "away": "Australia", "date": "2022-12-03 19:00", "stage": "Round of 16", "home_score": 2, "away_score": 1},
            {"home": "France", "away": "Poland", "date": "2022-12-04 15:00", "stage": "Round of 16", "home_score": 3, "away_score": 1},
            {"home": "England", "away": "Senegal", "date": "2022-12-04 19:00", "stage": "Round of 16", "home_score": 3, "away_score": 0},
            {"home": "Japan", "away": "Croatia", "date": "2022-12-05 15:00", "stage": "Round of 16", "home_score": 1, "away_score": 3},
            {"home": "Brazil", "away": "South Korea", "date": "2022-12-05 19:00", "stage": "Round of 16", "home_score": 4, "away_score": 1},
            {"home": "Morocco", "away": "Spain", "date": "2022-12-06 15:00", "stage": "Round of 16", "home_score": 0, "away_score": 0},
            {"home": "Portugal", "away": "Switzerland", "date": "2022-12-06 19:00", "stage": "Round of 16", "home_score": 6, "away_score": 1},
            
            # QUARTER-FINALS
            {"home": "Croatia", "away": "Brazil", "date": "2022-12-09 15:00", "stage": "Quarter-final", "home_score": 1, "away_score": 1},
            {"home": "Netherlands", "away": "Argentina", "date": "2022-12-09 19:00", "stage": "Quarter-final", "home_score": 2, "away_score": 2},
            {"home": "Morocco", "away": "Portugal", "date": "2022-12-10 15:00", "stage": "Quarter-final", "home_score": 1, "away_score": 0},
            {"home": "England", "away": "France", "date": "2022-12-10 19:00", "stage": "Quarter-final", "home_score": 1, "away_score": 2},
            
            # SEMI-FINALS
            {"home": "Argentina", "away": "Croatia", "date": "2022-12-13 19:00", "stage": "Semi-final", "home_score": 3, "away_score": 0},
            {"home": "France", "away": "Morocco", "date": "2022-12-14 19:00", "stage": "Semi-final", "home_score": 2, "away_score": 0},
            
            # THIRD PLACE PLAYOFF
            {"home": "Croatia", "away": "Morocco", "date": "2022-12-17 15:00", "stage": "Third Place Playoff", "home_score": 2, "away_score": 1},
            
            # FINAL
            {"home": "Argentina", "away": "France", "date": "2022-12-18 15:00", "stage": "Final", "home_score": 3, "away_score": 3}
        ]
        
        for match_data in matches_data:
            home_team = self.teams[match_data["home"]]
            away_team = self.teams[match_data["away"]]
            scheduled_time = datetime.strptime(match_data["date"], "%Y-%m-%d %H:%M")
            scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)
            
            match = Match(
                id=uuid.uuid4(),
                competition_id=self.competition_id,
                home_team_id=home_team.id,
                away_team_id=away_team.id,
                scheduled_at=scheduled_time,
                started_at=scheduled_time,
                finished_at=scheduled_time + timedelta(hours=2),
                venue="Stadium in Qatar",
                status=validate_enum_value(MatchStatus, "finished", f"for match {match_data.get('description', 'World Cup match')}"),
                home_score=match_data["home_score"],
                away_score=match_data["away_score"],
                referee="FIFA Referee",
                weather_conditions="Clear",
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            self.db.add(match)
            self.db.flush()  # Get the match ID
            
            # Create result
            result = Result(
                id=uuid.uuid4(),
                match_id=match.id,
                home_score=match_data["home_score"],
                away_score=match_data["away_score"],
                status=validate_enum_value(ResultStatus, "final", f"for result of match {match_data.get('description', 'World Cup match')}"),
                is_official=True,
                started_at=scheduled_time,
                finished_at=scheduled_time + timedelta(hours=2),
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            self.db.add(match)
        
        self.db.commit()
        print(f"✅ Created {len(matches_data)} key matches with results")
    
    def run_seed(self):
        """Run the complete seeding process."""
        print("🌱 Starting World Cup 2022 data seeding...")
        print("=" * 50)
        
        try:
            self.clear_existing_data()
            self.create_sport()
            self.create_season()
            self.create_teams()
            self.create_competition()
            self.create_key_players()
            self.create_sample_users()
            self.create_sample_groups()
            self.create_key_matches()
            
            print("=" * 50)
            print("🎉 Seeding completed successfully!")
            print(f"📊 Summary:")
            print(f"   • 100+ Players from all World Cup teams")
            print(f"   • 64 Complete World Cup 2022 Matches with Results")
            
        except Exception as e:
            print(f"❌ Error during seeding: {e}")
            self.db.rollback()
            raise
        finally:
            self.db.close()


if __name__ == "__main__":
    seeder = WorldCupSeeder()
    seeder.run_seed()