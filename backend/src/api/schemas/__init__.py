"""
Pydantic schemas package for API request/response models.

This module organizes all Pydantic schemas for the betting platform API,
providing consistent validation and serialization across all endpoints.
"""

from .user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserPasswordUpdate,
    UserResponse,
    UserProfile,
    UserSummary,
    UserLogin,
    UserLoginResponse,
    UserRegistrationResponse
)

from .group import (
    GroupBase,
    GroupCreate,
    GroupUpdate,
    GroupResponse,
    GroupSummary,
    GroupWithStats
)

from .sport import (
    SportBase,
    SportCreate,
    SportUpdate,
    SportResponse,
    SportSummary,
    SportWithStats
)

from .team import (
    TeamBase,
    TeamCreate,
    TeamUpdate,
    TeamResponse,
    TeamSummary,
    TeamWithStats,
    TeamWithSport
)

from .competition import (
    CompetitionBase,
    CompetitionCreate,
    CompetitionUpdate,
    CompetitionResponse,
    CompetitionSummary,
    CompetitionWithStats,
    CompetitionWithSport,
    CompetitionTeamRegistration,
    CompetitionTeamList,
    CompetitionStatus,
    CompetitionFormat
)

from .season import (
    SeasonBase,
    SeasonCreate,
    SeasonUpdate,
    SeasonResponse,
    SeasonSummary,
    SeasonWithStats,
    SeasonCompetitionList,
    SeasonStandings,
    SeasonStatus,
    SeasonType
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserPasswordUpdate",
    "UserResponse",
    "UserProfile",
    "UserSummary",
    "UserLogin",
    "UserLoginResponse",
    "UserRegistrationResponse",
    
    # Group schemas
    "GroupBase",
    "GroupCreate",
    "GroupUpdate",
    "GroupResponse",
    "GroupSummary",
    "GroupWithStats",
    
    # Sport schemas
    "SportBase",
    "SportCreate",
    "SportUpdate",
    "SportResponse",
    "SportSummary",
    "SportWithStats",
    
    # Team schemas
    "TeamBase",
    "TeamCreate",
    "TeamUpdate",
    "TeamResponse",
    "TeamSummary",
    "TeamWithStats",
    "TeamWithSport",
    
    # Competition schemas
    "CompetitionBase",
    "CompetitionCreate",
    "CompetitionUpdate",
    "CompetitionResponse",
    "CompetitionSummary",
    "CompetitionWithStats",
    "CompetitionWithSport",
    "CompetitionTeamRegistration",
    "CompetitionTeamList",
    "CompetitionStatus",
    "CompetitionFormat",
    
    # Season schemas
    "SeasonBase",
    "SeasonCreate",
    "SeasonUpdate",
    "SeasonResponse",
    "SeasonSummary",
    "SeasonWithStats",
    "SeasonCompetitionList",
    "SeasonStandings",
    "SeasonStatus",
    "SeasonType",
]