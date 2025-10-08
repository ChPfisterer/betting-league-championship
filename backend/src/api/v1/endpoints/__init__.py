"""
API v1 endpoints module.

This module imports and exposes all API endpoints for version 1.
"""

from . import (
    auth,
    keycloak_auth,
    users, 
    groups,
    sports,
    teams,
    competitions,
    seasons,
    matches,
    players,
    bets,
    predictions,  # New prediction endpoints
    results,
    group_memberships,
    audit_logs
)

__all__ = [
    "auth",
    "keycloak_auth",
    "users", 
    "groups",
    "sports",
    "teams",
    "competitions",
    "matches", 
    "seasons",
    "players",
    "bets",
    "predictions",  # New prediction endpoints
    "results",
    "group_memberships",
    "audit_logs"
]