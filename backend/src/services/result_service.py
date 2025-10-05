"""
Result service for managing match results and outcomes.

This service provides comprehensive business logic for handling match results,
including creation, validation, confirmation, dispute management, and automatic
bet settlement integration.
"""

from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID

from sqlalchemy import and_, or_, desc, asc, func, case, String
from sqlalchemy.orm import Session, joinedload

from models import Result, Match, User, Bet
from api.schemas.result import (
    ResultCreate,
    ResultUpdate,
    ResultConfirmation,
    ResultDispute,
    ResultOutcome,
    ResultStatistics,
    ResultAnalytics,
    ResultBulkCreate,
    ResultType,
    ResultStatus
)


class ResultService:
    """Service for managing match results and outcomes."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_result(self, result_data: ResultCreate) -> Result:
        """
        Create a new match result.
        
        Args:
            result_data: Result creation data
            
        Returns:
            Created result
            
        Raises:
            ValueError: If validation fails
        """
        # Validate match exists
        match = self.db.query(Match).filter(Match.id == result_data.match_id).first()
        if not match:
            raise ValueError(f"Match with ID {result_data.match_id} not found")
        
        # Check if result already exists for this match and type
        existing_result = self.db.query(Result).filter(
            and_(
                Result.match_id == result_data.match_id,
                Result.result_type == result_data.result_type
            )
        ).first()
        
        if existing_result:
            raise ValueError(
                f"Result of type {result_data.result_type} already exists for match {result_data.match_id}"
            )
        
        # Validate user exists
        user = self.db.query(User).filter(User.id == result_data.recorded_by).first()
        if not user:
            raise ValueError(f"User with ID {result_data.recorded_by} not found")
        
        # Validate scores if provided
        if result_data.home_score is not None and result_data.away_score is not None:
            if result_data.home_score < 0 or result_data.away_score < 0:
                raise ValueError("Scores cannot be negative")
        
        # Create result
        db_result = Result(
            match_id=result_data.match_id,
            result_type=result_data.result_type,
            home_score=result_data.home_score,
            away_score=result_data.away_score,
            status=result_data.status,
            additional_data=result_data.additional_data,
            notes=result_data.notes,
            recorded_by=result_data.recorded_by,
            recorded_at=datetime.utcnow()
        )
        
        self.db.add(db_result)
        self.db.commit()
        self.db.refresh(db_result)
        
        # If result is confirmed, trigger bet settlement
        if result_data.status == ResultStatus.CONFIRMED:
            self._trigger_bet_settlement(db_result)
        
        return db_result
    
    def get_result(self, result_id: UUID) -> Optional[Result]:
        """Get result by ID."""
        return self.db.query(Result).filter(Result.id == result_id).first()
    
    def list_results(
        self,
        skip: int = 0,
        limit: int = 100,
        match_id: Optional[UUID] = None,
        result_type: Optional[ResultType] = None,
        status: Optional[ResultStatus] = None,
        recorded_by: Optional[UUID] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None
    ) -> List[Result]:
        """
        List results with filtering options.
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            match_id: Filter by match ID
            result_type: Filter by result type
            status: Filter by result status
            recorded_by: Filter by user who recorded result
            date_from: Filter results from this date
            date_to: Filter results until this date
            
        Returns:
            List of results
        """
        query = self.db.query(Result)
        
        # Apply filters
        if match_id:
            query = query.filter(Result.match_id == match_id)
        
        if result_type:
            query = query.filter(Result.result_type == result_type)
        
        if status:
            query = query.filter(Result.status == status)
        
        if recorded_by:
            query = query.filter(Result.recorded_by == recorded_by)
        
        if date_from:
            query = query.filter(Result.recorded_at >= date_from)
        
        if date_to:
            query = query.filter(Result.recorded_at <= date_to)
        
        # Order by recorded date (newest first)
        query = query.order_by(desc(Result.recorded_at))
        
        return query.offset(skip).limit(limit).all()
    
    def update_result(self, result_id: UUID, update_data: ResultUpdate) -> Optional[Result]:
        """
        Update result data.
        
        Args:
            result_id: Result unique identifier
            update_data: Updated result data
            
        Returns:
            Updated result or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        result = self.get_result(result_id)
        if not result:
            return None
        
        # Validate that result can be updated
        if result.status == ResultStatus.CONFIRMED:
            raise ValueError("Cannot update confirmed result")
        
        # Validate scores if provided
        if update_data.home_score is not None and update_data.away_score is not None:
            if update_data.home_score < 0 or update_data.away_score < 0:
                raise ValueError("Scores cannot be negative")
        
        # Update fields
        if update_data.home_score is not None:
            result.home_score = update_data.home_score
        
        if update_data.away_score is not None:
            result.away_score = update_data.away_score
        
        if update_data.status is not None:
            result.status = update_data.status
        
        if update_data.additional_data is not None:
            result.additional_data = update_data.additional_data
        
        if update_data.notes is not None:
            result.notes = update_data.notes
        
        result.updated_at = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(result)
        
        # If result is now confirmed, trigger bet settlement
        if update_data.status == ResultStatus.CONFIRMED:
            result.confirmed_at = datetime.utcnow()
            self.db.commit()
            self._trigger_bet_settlement(result)
        
        return result
    
    def confirm_result(self, result_id: UUID, confirmation: ResultConfirmation) -> Optional[Result]:
        """
        Confirm a result.
        
        Args:
            result_id: Result unique identifier
            confirmation: Confirmation data
            
        Returns:
            Confirmed result or None if not found
            
        Raises:
            ValueError: If validation fails
        """
        result = self.get_result(result_id)
        if not result:
            return None
        
        if result.status == ResultStatus.CONFIRMED:
            raise ValueError("Result is already confirmed")
        
        if confirmation.confirmed:
            # Validate result before confirming
            validation = self.validate_result(result_id)
            
            if not validation["is_valid"] and not confirmation.override_validation:
                raise ValueError(
                    f"Cannot confirm invalid result. Errors: {', '.join(validation['validation_errors'])}"
                )
            
            result.status = ResultStatus.CONFIRMED
            result.confirmed_at = datetime.utcnow()
            
            if confirmation.confirmation_notes:
                if result.notes:
                    result.notes += f"\nConfirmation: {confirmation.confirmation_notes}"
                else:
                    result.notes = f"Confirmation: {confirmation.confirmation_notes}"
            
            self.db.commit()
            self.db.refresh(result)
            
            # Trigger bet settlement
            self._trigger_bet_settlement(result)
        
        return result
    
    def dispute_result(self, result_id: UUID, dispute: ResultDispute) -> Optional[Result]:
        """
        Dispute a result.
        
        Args:
            result_id: Result unique identifier
            dispute: Dispute data
            
        Returns:
            Disputed result or None if not found
        """
        result = self.get_result(result_id)
        if not result:
            return None
        
        # Update result status to disputed
        result.status = ResultStatus.DISPUTED
        result.updated_at = datetime.utcnow()
        
        # Add dispute information to additional data
        if not result.additional_data:
            result.additional_data = {}
        
        if "disputes" not in result.additional_data:
            result.additional_data["disputes"] = []
        
        dispute_record = {
            "dispute_reason": dispute.dispute_reason,
            "disputed_by": str(dispute.disputed_by),
            "disputed_at": datetime.utcnow().isoformat(),
            "evidence": dispute.evidence,
            "priority": dispute.priority
        }
        
        result.additional_data["disputes"].append(dispute_record)
        
        self.db.commit()
        self.db.refresh(result)
        
        return result
    
    def validate_result(self, result_id: UUID) -> Dict[str, Any]:
        """
        Validate a result.
        
        Args:
            result_id: Result unique identifier
            
        Returns:
            Validation result with errors and warnings
        """
        result = self.get_result(result_id)
        if not result:
            return {
                "result_id": result_id,
                "is_valid": False,
                "validation_errors": ["Result not found"],
                "validation_warnings": [],
                "suggested_corrections": None
            }
        
        errors = []
        warnings = []
        suggestions = {}
        
        # Validate scores
        if result.home_score is None or result.away_score is None:
            errors.append("Both home and away scores must be provided")
        elif result.home_score < 0 or result.away_score < 0:
            errors.append("Scores cannot be negative")
        
        # Validate match relationship
        match = self.db.query(Match).filter(Match.id == result.match_id).first()
        if not match:
            errors.append("Associated match not found")
        elif match.status != "completed":
            warnings.append("Match status is not 'completed'")
        
        # Check for duplicate results
        duplicate = self.db.query(Result).filter(
            and_(
                Result.match_id == result.match_id,
                Result.result_type == result.result_type,
                Result.id != result.id
            )
        ).first()
        
        if duplicate:
            errors.append(f"Duplicate result exists for this match and type")
        
        # Validate additional data structure
        if result.additional_data:
            try:
                import json
                json.dumps(result.additional_data)
            except (TypeError, ValueError):
                errors.append("Additional data is not JSON-serializable")
        
        return {
            "result_id": result_id,
            "is_valid": len(errors) == 0,
            "validation_errors": errors,
            "validation_warnings": warnings,
            "suggested_corrections": suggestions if suggestions else None
        }
    
    def calculate_outcome(self, result_id: UUID) -> Optional[ResultOutcome]:
        """
        Calculate match outcome from result.
        
        Args:
            result_id: Result unique identifier
            
        Returns:
            Result outcome data
        """
        result = self.get_result(result_id)
        if not result or result.home_score is None or result.away_score is None:
            return None
        
        home_score = result.home_score
        away_score = result.away_score
        total_goals = home_score + away_score
        
        # Determine match result
        if home_score > away_score:
            match_result = "home_win"
        elif away_score > home_score:
            match_result = "away_win"
        else:
            match_result = "draw"
        
        # Calculate additional outcome data
        outcome_data = {
            "winning_margin": abs(home_score - away_score),
            "over_under_2_5": "over" if total_goals > 2.5 else "under",
            "over_under_1_5": "over" if total_goals > 1.5 else "under",
            "over_under_3_5": "over" if total_goals > 3.5 else "under",
            "both_teams_scored": home_score > 0 and away_score > 0,
            "clean_sheet_home": away_score == 0,
            "clean_sheet_away": home_score == 0,
            "high_scoring": total_goals >= 4,
            "low_scoring": total_goals <= 1
        }
        
        return ResultOutcome(
            result_id=result_id,
            match_result=match_result,
            total_goals=total_goals,
            both_teams_scored=outcome_data["both_teams_scored"],
            clean_sheet=outcome_data["clean_sheet_home"] or outcome_data["clean_sheet_away"],
            outcome_data=outcome_data
        )
    
    def get_match_results(self, match_id: UUID) -> List[Result]:
        """Get all results for a specific match."""
        return self.db.query(Result).filter(Result.match_id == match_id).all()
    
    def get_user_results(self, user_id: UUID, limit: int = 100) -> List[Result]:
        """Get results recorded by a specific user."""
        return (
            self.db.query(Result)
            .filter(Result.recorded_by == user_id)
            .order_by(desc(Result.recorded_at))
            .limit(limit)
            .all()
        )
    
    def get_pending_results(self, limit: int = 100) -> List[Result]:
        """Get pending results that need confirmation."""
        return (
            self.db.query(Result)
            .filter(Result.status == ResultStatus.PENDING)
            .order_by(asc(Result.recorded_at))
            .limit(limit)
            .all()
        )
    
    def get_disputed_results(self, limit: int = 100) -> List[Result]:
        """Get disputed results that need resolution."""
        return (
            self.db.query(Result)
            .filter(Result.status == ResultStatus.DISPUTED)
            .order_by(asc(Result.recorded_at))
            .limit(limit)
            .all()
        )
    
    def get_statistics(self, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> ResultStatistics:
        """
        Get result statistics.
        
        Args:
            date_from: Filter from this date
            date_to: Filter until this date
            
        Returns:
            Result statistics
        """
        query = self.db.query(Result)
        
        if date_from:
            query = query.filter(Result.recorded_at >= date_from)
        
        if date_to:
            query = query.filter(Result.recorded_at <= date_to)
        
        # Get basic counts
        total_results = query.count()
        confirmed_results = query.filter(Result.status == ResultStatus.CONFIRMED).count()
        pending_results = query.filter(Result.status == ResultStatus.PENDING).count()
        disputed_results = query.filter(Result.status == ResultStatus.DISPUTED).count()
        
        # Get confirmed results for detailed statistics
        confirmed_query = query.filter(
            and_(
                Result.status == ResultStatus.CONFIRMED,
                Result.home_score.isnot(None),
                Result.away_score.isnot(None)
            )
        )
        
        confirmed_data = confirmed_query.all()
        
        if not confirmed_data:
            return ResultStatistics(
                total_results=total_results,
                confirmed_results=confirmed_results,
                pending_results=pending_results,
                disputed_results=disputed_results,
                average_goals_per_match=None,
                home_win_percentage=None,
                away_win_percentage=None,
                draw_percentage=None
            )
        
        # Calculate statistics
        total_goals = sum(r.home_score + r.away_score for r in confirmed_data)
        average_goals = Decimal(total_goals) / Decimal(len(confirmed_data))
        
        home_wins = sum(1 for r in confirmed_data if r.home_score > r.away_score)
        away_wins = sum(1 for r in confirmed_data if r.away_score > r.home_score)
        draws = sum(1 for r in confirmed_data if r.home_score == r.away_score)
        
        home_win_pct = Decimal(home_wins) / Decimal(len(confirmed_data)) * 100
        away_win_pct = Decimal(away_wins) / Decimal(len(confirmed_data)) * 100
        draw_pct = Decimal(draws) / Decimal(len(confirmed_data)) * 100
        
        return ResultStatistics(
            total_results=total_results,
            confirmed_results=confirmed_results,
            pending_results=pending_results,
            disputed_results=disputed_results,
            average_goals_per_match=average_goals.quantize(Decimal('0.01')),
            home_win_percentage=home_win_pct.quantize(Decimal('0.01')),
            away_win_percentage=away_win_pct.quantize(Decimal('0.01')),
            draw_percentage=draw_pct.quantize(Decimal('0.01'))
        )
    
    def get_analytics(self, period_days: int = 30) -> ResultAnalytics:
        """
        Get result analytics for a specific period.
        
        Args:
            period_days: Number of days to analyze
            
        Returns:
            Result analytics data
        """
        period_end = datetime.utcnow()
        period_start = period_end - timedelta(days=period_days)
        
        # Get confirmed results in period
        results = (
            self.db.query(Result)
            .filter(
                and_(
                    Result.status == ResultStatus.CONFIRMED,
                    Result.recorded_at >= period_start,
                    Result.recorded_at <= period_end,
                    Result.home_score.isnot(None),
                    Result.away_score.isnot(None)
                )
            )
            .all()
        )
        
        if not results:
            return ResultAnalytics(
                period_start=period_start,
                period_end=period_end,
                total_matches=0,
                total_goals=0,
                average_goals_per_match=Decimal('0'),
                home_wins=0,
                away_wins=0,
                draws=0,
                both_teams_scored_count=0,
                clean_sheets=0,
                highest_scoring_match=None,
                most_goals_by_team=None
            )
        
        # Calculate analytics
        total_goals = sum(r.home_score + r.away_score for r in results)
        average_goals = Decimal(total_goals) / Decimal(len(results))
        
        home_wins = sum(1 for r in results if r.home_score > r.away_score)
        away_wins = sum(1 for r in results if r.away_score > r.home_score)
        draws = sum(1 for r in results if r.home_score == r.away_score)
        
        both_teams_scored = sum(1 for r in results if r.home_score > 0 and r.away_score > 0)
        clean_sheets = sum(1 for r in results if r.home_score == 0 or r.away_score == 0)
        
        # Find highest scoring match
        highest_scoring = max(results, key=lambda r: r.home_score + r.away_score)
        highest_scoring_data = {
            "result_id": str(highest_scoring.id),
            "match_id": str(highest_scoring.match_id),
            "home_score": highest_scoring.home_score,
            "away_score": highest_scoring.away_score,
            "total_goals": highest_scoring.home_score + highest_scoring.away_score
        }
        
        # Find most goals by a team
        max_team_goals = max(
            max(r.home_score for r in results),
            max(r.away_score for r in results)
        )
        
        most_goals_match = next(
            r for r in results 
            if r.home_score == max_team_goals or r.away_score == max_team_goals
        )
        
        most_goals_data = {
            "result_id": str(most_goals_match.id),
            "match_id": str(most_goals_match.match_id),
            "goals": max_team_goals,
            "team": "home" if most_goals_match.home_score == max_team_goals else "away"
        }
        
        return ResultAnalytics(
            period_start=period_start,
            period_end=period_end,
            total_matches=len(results),
            total_goals=total_goals,
            average_goals_per_match=average_goals.quantize(Decimal('0.01')),
            home_wins=home_wins,
            away_wins=away_wins,
            draws=draws,
            both_teams_scored_count=both_teams_scored,
            clean_sheets=clean_sheets,
            highest_scoring_match=highest_scoring_data,
            most_goals_by_team=most_goals_data
        )
    
    def bulk_create_results(self, bulk_data: ResultBulkCreate) -> Dict[str, Any]:
        """
        Create multiple results in bulk.
        
        Args:
            bulk_data: Bulk creation data
            
        Returns:
            Bulk creation summary
        """
        created_results = []
        errors = []
        skipped_count = 0
        
        for i, result_data in enumerate(bulk_data.results):
            try:
                # Check for duplicates if skip_duplicates is enabled
                if bulk_data.skip_duplicates:
                    existing = self.db.query(Result).filter(
                        and_(
                            Result.match_id == result_data.match_id,
                            Result.result_type == result_data.result_type
                        )
                    ).first()
                    
                    if existing:
                        skipped_count += 1
                        continue
                
                # Validate before creating if validate_all is enabled
                if bulk_data.validate_all:
                    # Quick validation without creating the result
                    match = self.db.query(Match).filter(Match.id == result_data.match_id).first()
                    if not match:
                        errors.append({
                            "index": i,
                            "error": f"Match with ID {result_data.match_id} not found"
                        })
                        continue
                    
                    user = self.db.query(User).filter(User.id == result_data.recorded_by).first()
                    if not user:
                        errors.append({
                            "index": i,
                            "error": f"User with ID {result_data.recorded_by} not found"
                        })
                        continue
                
                # Create result
                result = self.create_result(result_data)
                created_results.append(result.id)
                
            except Exception as e:
                errors.append({
                    "index": i,
                    "error": str(e)
                })
        
        return {
            "created_count": len(created_results),
            "skipped_count": skipped_count,
            "error_count": len(errors),
            "created_results": created_results,
            "errors": errors
        }
    
    def delete_result(self, result_id: UUID) -> bool:
        """
        Delete a result.
        
        Args:
            result_id: Result unique identifier
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If result cannot be deleted
        """
        result = self.get_result(result_id)
        if not result:
            return False
        
        # Check if result is confirmed and has associated bets
        if result.status == ResultStatus.CONFIRMED:
            bets_count = self.db.query(Bet).filter(Bet.match_id == result.match_id).count()
            if bets_count > 0:
                raise ValueError("Cannot delete confirmed result with associated settled bets")
        
        self.db.delete(result)
        self.db.commit()
        return True
    
    def search_results(self, query: str, limit: int = 100) -> List[Result]:
        """
        Search results by notes or additional data.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching results
        """
        search_term = f"%{query}%"
        
        return (
            self.db.query(Result)
            .filter(
                or_(
                    Result.notes.ilike(search_term),
                    func.cast(Result.additional_data, String).ilike(search_term)
                )
            )
            .order_by(desc(Result.recorded_at))
            .limit(limit)
            .all()
        )
    
    def _trigger_bet_settlement(self, result: Result) -> None:
        """
        Trigger automatic bet settlement for confirmed result.
        
        Args:
            result: Confirmed result
        """
        # This would typically call the bet service to settle bets
        # For now, we'll just update match status if needed
        
        # Get associated match
        match = self.db.query(Match).filter(Match.id == result.match_id).first()
        if match and match.status != "completed":
            match.status = "completed"
            match.home_score = result.home_score
            match.away_score = result.away_score
            self.db.commit()
        
        # Note: In a full implementation, this would call BetService.auto_settle_match_bets()
        # to automatically settle all bets for this match based on the result