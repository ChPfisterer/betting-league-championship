"""
Player API endpoints for the betting platform.

This module provides comprehensive CRUD operations for player management,
including creation, listing, updating, team associations, transfers,
statistics, and search functionality. Players are individual athletes
in the betting platform ecosystem.
"""

from typing import List, Optional
from uuid import UUID
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from core import get_db, get_current_user, http_not_found, http_conflict
from models import User, Player, Team, Sport
from api.schemas.player import (
    PlayerCreate,
    PlayerUpdate,
    PlayerTransferCreate,
    PlayerContractUpdate,
    PlayerResponse,
    PlayerSummary,
    PlayerWithStats,
    PlayerWithTeam,
    PlayerWithHistory,
    PlayerTransferResponse,
    PlayerPosition,
    PlayerStatus
)
from services.player_service import PlayerService


router = APIRouter()


@router.post(
    "/",
    response_model=PlayerResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Player",
    description="Create a new player with comprehensive validation"
)
async def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerResponse:
    """
    Create a new player.
    
    Args:
        player_data: Player creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Created player details
        
    Raises:
        HTTPException: If validation fails
    """
    service = PlayerService(db)
    player = service.create_player(player_data)
    return PlayerResponse.model_validate(player)


@router.get(
    "/",
    response_model=List[PlayerSummary],
    summary="List Players",
    description="List players with comprehensive filtering options"
)
async def list_players(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    team_id: Optional[UUID] = Query(None, description="Filter by team ID"),
    sport_id: Optional[UUID] = Query(None, description="Filter by sport ID"),
    position: Optional[PlayerPosition] = Query(None, description="Filter by position"),
    status: Optional[PlayerStatus] = Query(None, description="Filter by player status"),
    nationality: Optional[str] = Query(None, description="Filter by nationality"),
    min_age: Optional[int] = Query(None, ge=16, le=50, description="Minimum age filter"),
    max_age: Optional[int] = Query(None, ge=16, le=50, description="Maximum age filter"),
    is_captain: Optional[bool] = Query(None, description="Filter by captain status"),
    is_vice_captain: Optional[bool] = Query(None, description="Filter by vice-captain status"),
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    List players with filtering options.
    
    Args:
        skip: Number of records to skip for pagination
        limit: Maximum number of records to return
        team_id: Filter by team ID
        sport_id: Filter by sport ID
        position: Filter by position
        status: Filter by player status
        nationality: Filter by nationality
        min_age: Minimum age filter
        max_age: Maximum age filter
        is_captain: Filter by captain status
        is_vice_captain: Filter by vice-captain status
        db: Database session
        
    Returns:
        List of player summaries
    """
    service = PlayerService(db)
    players = service.list_players(
        skip=skip,
        limit=limit,
        team_id=team_id,
        sport_id=sport_id,
        position=position,
        status=status,
        nationality=nationality,
        min_age=min_age,
        max_age=max_age,
        is_captain=is_captain,
        is_vice_captain=is_vice_captain
    )
    return [PlayerSummary.model_validate(player) for player in players]


@router.get(
    "/active",
    response_model=List[PlayerSummary],
    summary="List Active Players",
    description="Get all currently active players"
)
async def list_active_players(
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    Get active players.
    
    Args:
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of active player summaries
    """
    service = PlayerService(db)
    players = service.get_active_players(limit=limit)
    return [PlayerSummary.model_validate(player) for player in players]


@router.get(
    "/free-agents",
    response_model=List[PlayerSummary],
    summary="List Free Agents",
    description="Get players without team assignments"
)
async def list_free_agents(
    sport_id: Optional[UUID] = Query(None, description="Filter by sport ID"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    Get free agent players.
    
    Args:
        sport_id: Filter by sport ID
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of free agent player summaries
    """
    service = PlayerService(db)
    players = service.get_free_agents(sport_id=sport_id, limit=limit)
    return [PlayerSummary.model_validate(player) for player in players]


@router.get(
    "/by-position/{position}",
    response_model=List[PlayerSummary],
    summary="List Players by Position",
    description="Get players by specific position"
)
async def list_players_by_position(
    position: PlayerPosition,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    Get players by position.
    
    Args:
        position: Player position
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of players in the position
    """
    service = PlayerService(db)
    players = service.get_players_by_position(position, limit=limit)
    return [PlayerSummary.model_validate(player) for player in players]


@router.get(
    "/{player_id}",
    response_model=PlayerResponse,
    summary="Get Player",
    description="Get player details by ID"
)
async def get_player(
    player_id: UUID,
    db: Session = Depends(get_db)
) -> PlayerResponse:
    """
    Get player by ID.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        
    Returns:
        Player details
        
    Raises:
        HTTPException: If player not found
    """
    service = PlayerService(db)
    player = service.get_player(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerResponse.model_validate(player)


@router.get(
    "/{player_id}/stats",
    response_model=PlayerWithStats,
    summary="Get Player Statistics",
    description="Get comprehensive player statistics"
)
async def get_player_statistics(
    player_id: UUID,
    db: Session = Depends(get_db)
) -> PlayerWithStats:
    """
    Get player statistics.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        
    Returns:
        Player details with statistics
        
    Raises:
        HTTPException: If player not found
    """
    service = PlayerService(db)
    player = service.get_player(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    stats = service.get_player_statistics(player_id)
    
    # Create response with stats
    player_dict = PlayerResponse.model_validate(player).model_dump()
    player_dict['stats'] = stats
    
    return PlayerWithStats.model_validate(player_dict)


@router.get(
    "/{player_id}/with-team",
    response_model=PlayerWithTeam,
    summary="Get Player with Team",
    description="Get player details including team information"
)
async def get_player_with_team(
    player_id: UUID,
    db: Session = Depends(get_db)
) -> PlayerWithTeam:
    """
    Get player with team details.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        
    Returns:
        Player details with team information
        
    Raises:
        HTTPException: If player not found
    """
    service = PlayerService(db)
    player = service.get_player(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
    
    # Load team relationship if exists
    team = None
    if player.team_id:
        team = db.query(Team).filter(Team.id == player.team_id).first()
    
    player_dict = PlayerResponse.model_validate(player).model_dump()
    player_dict['team'] = team
    
    return PlayerWithTeam.model_validate(player_dict)


@router.get(
    "/{player_id}/history",
    response_model=PlayerWithHistory,
    summary="Get Player History",
    description="Get player details including transfer/contract history"
)
async def get_player_history(
    player_id: UUID,
    db: Session = Depends(get_db)
) -> PlayerWithHistory:
    """
    Get player with history.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        
    Returns:
        Player details with history information
        
    Raises:
        HTTPException: If player not found
    """
    service = PlayerService(db)
    player = service.get_player(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
    
    # Get transfer and contract history
    history = service.get_player_history(player_id)
    
    player_dict = PlayerResponse.model_validate(player).model_dump()
    player_dict['transfer_history'] = history.get('transfers', [])
    player_dict['contract_history'] = history.get('contracts', [])
    
    return PlayerWithHistory.model_validate(player_dict)


@router.get(
    "/team/{team_id}",
    response_model=List[PlayerSummary],
    summary="List Players by Team",
    description="Get all players for a specific team"
)
async def list_players_by_team(
    team_id: UUID,
    include_inactive: bool = Query(False, description="Include inactive players"),
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    Get players by team.
    
    Args:
        team_id: Team unique identifier
        include_inactive: Include inactive players
        db: Database session
        
    Returns:
        List of players for the team
    """
    service = PlayerService(db)
    players = service.get_players_by_team(team_id, include_inactive=include_inactive)
    return [PlayerSummary.model_validate(player) for player in players]


@router.get(
    "/team/{team_id}/captains",
    response_model=List[PlayerSummary],
    summary="Get Team Captains",
    description="Get captain and vice-captain for a team"
)
async def get_team_captains(
    team_id: UUID,
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    Get team captains.
    
    Args:
        team_id: Team unique identifier
        db: Database session
        
    Returns:
        List of team captains (captain and vice-captain)
    """
    service = PlayerService(db)
    captains = service.get_team_captains(team_id)
    return [PlayerSummary.model_validate(player) for player in captains]


@router.put(
    "/{player_id}",
    response_model=PlayerResponse,
    summary="Update Player",
    description="Update player details with validation"
)
async def update_player(
    player_id: UUID,
    update_data: PlayerUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerResponse:
    """
    Update player.
    
    Args:
        player_id: Player unique identifier
        update_data: Updated player data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated player details
        
    Raises:
        HTTPException: If player not found or validation fails
    """
    service = PlayerService(db)
    player = service.update_player(player_id, update_data)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerResponse.model_validate(player)


@router.patch(
    "/{player_id}/contract",
    response_model=PlayerResponse,
    summary="Update Player Contract",
    description="Update player contract details"
)
async def update_player_contract(
    player_id: UUID,
    contract_data: PlayerContractUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerResponse:
    """
    Update player contract.
    
    Args:
        player_id: Player unique identifier
        contract_data: Contract update data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated player details
        
    Raises:
        HTTPException: If player not found
    """
    service = PlayerService(db)
    player = service.update_contract(player_id, contract_data)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerResponse.model_validate(player)


@router.post(
    "/{player_id}/transfer",
    response_model=PlayerTransferResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Transfer Player",
    description="Transfer player to a new team"
)
async def transfer_player(
    player_id: UUID,
    transfer_data: PlayerTransferCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerTransferResponse:
    """
    Transfer player to new team.
    
    Args:
        player_id: Player unique identifier
        transfer_data: Transfer details
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Transfer confirmation details
        
    Raises:
        HTTPException: If player not found or transfer invalid
    """
    service = PlayerService(db)
    transfer = service.transfer_player(player_id, transfer_data)
    
    if not transfer:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerTransferResponse.model_validate(transfer)


@router.patch(
    "/{player_id}/captain",
    response_model=PlayerResponse,
    summary="Set Player as Captain",
    description="Designate player as team captain"
)
async def set_captain(
    player_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerResponse:
    """
    Set player as captain.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated player details
        
    Raises:
        HTTPException: If player not found or cannot be captain
    """
    service = PlayerService(db)
    player = service.set_captain(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerResponse.model_validate(player)


@router.patch(
    "/{player_id}/vice-captain",
    response_model=PlayerResponse,
    summary="Set Player as Vice-Captain",
    description="Designate player as team vice-captain"
)
async def set_vice_captain(
    player_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerResponse:
    """
    Set player as vice-captain.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated player details
        
    Raises:
        HTTPException: If player not found or cannot be vice-captain
    """
    service = PlayerService(db)
    player = service.set_vice_captain(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerResponse.model_validate(player)


@router.patch(
    "/{player_id}/remove-captaincy",
    response_model=PlayerResponse,
    summary="Remove Player Captaincy",
    description="Remove captain/vice-captain status from player"
)
async def remove_captaincy(
    player_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> PlayerResponse:
    """
    Remove captaincy from player.
    
    Args:
        player_id: Player unique identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        Updated player details
        
    Raises:
        HTTPException: If player not found
    """
    service = PlayerService(db)
    player = service.remove_captaincy(player_id)
    
    if not player:
        raise http_not_found(f"Player with ID {player_id} not found")
        
    return PlayerResponse.model_validate(player)


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Player",
    description="Soft delete player (sets as inactive)"
)
async def delete_player(
    player_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
) -> None:
    """
    Delete player (soft delete).
    
    Args:
        player_id: Player unique identifier
        db: Database session
        current_user: Authenticated user
        
    Raises:
        HTTPException: If player not found or cannot be deleted
    """
    service = PlayerService(db)
    deleted = service.delete_player(player_id)
    
    if not deleted:
        raise http_not_found(f"Player with ID {player_id} not found")


@router.get(
    "/search/{query}",
    response_model=List[PlayerSummary],
    summary="Search Players",
    description="Search players by name, nationality, or position"
)
async def search_players(
    query: str,
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: Session = Depends(get_db)
) -> List[PlayerSummary]:
    """
    Search players.
    
    Args:
        query: Search query string
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of matching players
    """
    service = PlayerService(db)
    players = service.search_players(query, limit=limit)
    return [PlayerSummary.model_validate(player) for player in players]
