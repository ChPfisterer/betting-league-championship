"""
API version 1 router configuration.

This module organizes all v1 API endpoints and provides
a centralized router for the betting platform API.
"""

from fastapi import APIRouter

from .endpoints import (
    users,
    groups,
    sports,
    teams,
    competitions,
    matches,
    seasons,
    players,
    bets,
    predictions,  # New prediction endpoints
    results,
    group_memberships,
    audit_logs,
    auth,
    keycloak_auth
)

# Create the main v1 API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router, 
    prefix="/auth", 
    tags=["Authentication"]
)

api_router.include_router(
    keycloak_auth.router, 
    prefix="/auth/keycloak", 
    tags=["Keycloak OAuth"]
)

api_router.include_router(
    users.router, 
    prefix="/users", 
    tags=["Users"]
)

api_router.include_router(
    groups.router, 
    prefix="/groups", 
    tags=["Groups"]
)

api_router.include_router(
    sports.router, 
    prefix="/sports", 
    tags=["Sports"]
)

api_router.include_router(
    teams.router, 
    prefix="/teams", 
    tags=["Teams"]
)

api_router.include_router(
    competitions.router, 
    prefix="/competitions", 
    tags=["Competitions"]
)

api_router.include_router(
    matches.router, 
    prefix="/matches", 
    tags=["Matches"]
)

api_router.include_router(
    seasons.router, 
    prefix="/seasons", 
    tags=["Seasons"]
)

api_router.include_router(
    players.router, 
    prefix="/players", 
    tags=["Players"]
)

api_router.include_router(
    bets.router, 
    prefix="/bets", 
    tags=["Bets"]
)

api_router.include_router(
    predictions.router, 
    prefix="/predictions", 
    tags=["Predictions"]
)

api_router.include_router(
    results.router, 
    prefix="/results", 
    tags=["Results"]
)

api_router.include_router(
    group_memberships.router, 
    prefix="/group-memberships", 
    tags=["Group Memberships"]
)

api_router.include_router(
    audit_logs.router, 
    prefix="/audit-logs", 
    tags=["Audit Logs"]
)

__all__ = ["api_router"]