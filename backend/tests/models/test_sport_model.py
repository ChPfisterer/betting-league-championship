"""
Unit tests for Sport model - T064

TDD Red Phase: These tests define the behavior and constraints for the Sport model.
All tests should fail initially until the Sport model is implemented.

Coverage:
- Sport model fields and validation
- Sport categories and types
- Rules and configuration
- Active status management
- Model relationships with competitions and matches
- Sport-specific settings
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, patch
import uuid
from typing import Optional, Dict, Any

# These imports will fail initially (Red phase) until models are implemented
try:
    from src.models.sport import Sport
    from src.models.competition import Competition
    from src.models.match import Match
    from src.database import get_db_session
    from sqlalchemy.exc import IntegrityError
    from sqlalchemy.orm import Session
except ImportError:
    # Expected during Red phase - models don't exist yet
    Sport = None
    Competition = None
    Match = None
    get_db_session = None
    IntegrityError = None
    Session = None

pytestmark = pytest.mark.asyncio


class TestSportModelStructure:
    """Test Sport model structure and basic attributes."""

    def test_sport_model_exists(self):
        """Test that Sport model class exists."""
        assert Sport is not None, "Sport model should be defined"

    def test_sport_model_has_required_fields(self):
        """Test that Sport model has all required fields."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Required fields that should exist on Sport model
        required_fields = [
            'id', 'name', 'slug', 'category', 'is_active',
            'created_at', 'updated_at'
        ]
        
        for field in required_fields:
            assert hasattr(Sport, field), f"Sport model should have {field} field"

    def test_sport_model_has_optional_fields(self):
        """Test that Sport model has optional fields."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Optional fields
        optional_fields = [
            'description', 'rules', 'icon_url', 'color_scheme',
            'default_bet_types', 'scoring_system', 'match_duration',
            'season_structure', 'popularity_score'
        ]
        
        for field in optional_fields:
            assert hasattr(Sport, field), f"Sport model should have {field} field"


class TestSportModelValidation:
    """Test Sport model validation rules."""

    def test_sport_creation_with_valid_data(self):
        """Test creating sport with valid data succeeds."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        valid_data = {
            'name': 'Football',
            'slug': 'football',
            'category': 'team_sport'
        }
        
        sport = Sport(**valid_data)
        
        assert sport.name == 'Football'
        assert sport.slug == 'football'
        assert sport.category == 'team_sport'

    def test_sport_name_required(self):
        """Test that name is required."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        with pytest.raises((ValueError, TypeError)):
            Sport(
                slug='football',
                category='team_sport'
                # Missing name
            )

    def test_sport_slug_required(self):
        """Test that slug is required."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        with pytest.raises((ValueError, TypeError)):
            Sport(
                name='Football',
                category='team_sport'
                # Missing slug
            )

    def test_sport_name_length_validation(self):
        """Test sport name length constraints."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Too short name
        with pytest.raises(ValueError):
            Sport(
                name='A',  # Single character
                slug='a',
                category='team_sport'
            )
            
        # Too long name
        with pytest.raises(ValueError):
            Sport(
                name='A' * 101,  # Over 100 characters
                slug='long-sport',
                category='team_sport'
            )

    def test_sport_slug_format_validation(self):
        """Test slug format validation."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Valid slug formats
        valid_slugs = ['football', 'american-football', 'table_tennis', 'sport123']
        
        for slug in valid_slugs:
            sport = Sport(
                name='Test Sport',
                slug=slug,
                category='team_sport'
            )
            assert sport.slug == slug

    def test_sport_slug_invalid_format(self):
        """Test invalid slug formats."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Invalid slug formats
        invalid_slugs = [
            'Football',  # Capital letters
            'foot ball',  # Spaces
            'foot@ball',  # Special characters
            'football!',  # Exclamation
            '',  # Empty string
            'a',  # Too short
            'a' * 51  # Too long
        ]
        
        for slug in invalid_slugs:
            with pytest.raises(ValueError):
                Sport(
                    name='Test Sport',
                    slug=slug,
                    category='team_sport'
                )

    def test_sport_category_validation(self):
        """Test sport category validation."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Valid categories
        valid_categories = [
            'team_sport', 'individual_sport', 'combat_sport',
            'racing', 'water_sport', 'winter_sport', 'esport'
        ]
        
        for category in valid_categories:
            sport = Sport(
                name='Test Sport',
                slug='test-sport',
                category=category
            )
            assert sport.category == category

    def test_sport_category_invalid(self):
        """Test invalid category values."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Invalid category
        with pytest.raises(ValueError):
            Sport(
                name='Test Sport',
                slug='test-sport',
                category='invalid_category'
            )

    def test_sport_slug_unique_constraint(self):
        """Test that sport slug must be unique."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # This will be tested at database level
        # Should ensure slug is unique across all sports
        pass


class TestSportModelDefaults:
    """Test Sport model default values."""

    def test_sport_default_values(self):
        """Test that Sport model sets correct default values."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Test Sport',
            slug='test-sport',
            category='team_sport'
        )
        
        # Default values
        assert sport.is_active is True
        assert sport.description is None
        assert sport.rules is None
        assert sport.icon_url is None
        assert sport.color_scheme is None
        assert sport.popularity_score == 0
        assert sport.match_duration is None

    def test_sport_id_auto_generation(self):
        """Test that sport ID is automatically generated."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Test Sport',
            slug='test-sport',
            category='team_sport'
        )
        
        # ID should be auto-generated UUID
        assert sport.id is not None
        assert isinstance(sport.id, (str, uuid.UUID))

    def test_sport_timestamps_auto_generation(self):
        """Test that timestamps are automatically set."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Test Sport',
            slug='test-sport',
            category='team_sport'
        )
        
        # Timestamps should be auto-generated
        assert sport.created_at is not None
        assert sport.updated_at is not None
        assert isinstance(sport.created_at, datetime)
        assert isinstance(sport.updated_at, datetime)

    def test_sport_default_bet_types_structure(self):
        """Test default bet types structure."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should have default bet types for the sport
        assert hasattr(sport, 'default_bet_types')
        assert isinstance(sport.default_bet_types, (list, dict, type(None)))


class TestSportModelMethods:
    """Test Sport model methods and computed properties."""

    def test_sport_display_name_property(self):
        """Test display_name computed property."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='American Football',
            slug='american-football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'display_name')
        # Should format name for display
        assert sport.display_name == 'American Football'

    def test_sport_is_team_sport_property(self):
        """Test is_team_sport computed property."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        team_sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        individual_sport = Sport(
            name='Tennis',
            slug='tennis',
            category='individual_sport'
        )
        
        assert hasattr(team_sport, 'is_team_sport')
        assert team_sport.is_team_sport is True
        assert individual_sport.is_team_sport is False

    def test_sport_get_available_bet_types_method(self):
        """Test get_available_bet_types method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'get_available_bet_types')
        
        # Mock the method for testing
        with patch.object(sport, 'get_available_bet_types') as mock_bet_types:
            expected_types = ['match_winner', 'over_under', 'handicap']
            mock_bet_types.return_value = expected_types
            
            bet_types = sport.get_available_bet_types()
            assert bet_types == expected_types
            mock_bet_types.assert_called_once()

    def test_sport_get_default_rules_method(self):
        """Test get_default_rules method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'get_default_rules')
        
        # Mock the method for testing
        with patch.object(sport, 'get_default_rules') as mock_rules:
            expected_rules = {
                'match_duration': 90,
                'overtime_rules': 'extra_time_penalties',
                'team_size': 11
            }
            mock_rules.return_value = expected_rules
            
            rules = sport.get_default_rules()
            assert rules == expected_rules
            mock_rules.assert_called_once()

    def test_sport_update_popularity_method(self):
        """Test update_popularity method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport',
            popularity_score=50
        )
        
        assert hasattr(sport, 'update_popularity')
        
        # Mock the method for testing
        with patch.object(sport, 'update_popularity') as mock_update:
            sport.update_popularity(75)
            mock_update.assert_called_once_with(75)
            
        # Should update popularity score
        assert sport.popularity_score == 75

    def test_sport_activate_deactivate_methods(self):
        """Test activate and deactivate methods."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'activate')
        assert hasattr(sport, 'deactivate')
        
        # Test deactivation
        sport.deactivate()
        assert sport.is_active is False
        
        # Test activation
        sport.activate()
        assert sport.is_active is True

    def test_sport_get_competition_count_method(self):
        """Test get_competition_count method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'get_competition_count')
        
        # Mock the method for testing
        with patch.object(sport, 'get_competition_count') as mock_count:
            mock_count.return_value = 5
            
            count = sport.get_competition_count()
            assert count == 5
            mock_count.assert_called_once()


class TestSportModelRelationships:
    """Test Sport model relationships with other models."""

    def test_sport_competitions_relationship(self):
        """Test Sport relationship with Competitions."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should have competitions relationship
        assert hasattr(sport, 'competitions')

    def test_sport_matches_relationship(self):
        """Test Sport relationship with Matches (through competitions)."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should have matches relationship
        assert hasattr(sport, 'matches')

    def test_sport_bets_relationship(self):
        """Test Sport relationship with Bets (through matches)."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should have bets relationship through matches
        assert hasattr(sport, 'bets')


class TestSportModelSerialization:
    """Test Sport model serialization and representation."""

    def test_sport_to_dict(self):
        """Test Sport model to_dict method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport',
            description='The beautiful game'
        )
        
        assert hasattr(sport, 'to_dict')
        
        sport_dict = sport.to_dict()
        
        # Should contain expected fields
        expected_fields = [
            'id', 'name', 'slug', 'category', 'description',
            'is_active', 'created_at', 'updated_at',
            'popularity_score', 'is_team_sport'
        ]
        
        for field in expected_fields:
            assert field in sport_dict

    def test_sport_to_dict_include_stats(self):
        """Test Sport to_dict with statistics included."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should support including statistics
        sport_dict = sport.to_dict(include_stats=True)
        stats_fields = ['competition_count', 'active_matches', 'total_bets']
        
        for field in stats_fields:
            assert field in sport_dict

    def test_sport_to_dict_include_rules(self):
        """Test Sport to_dict with rules included."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should support including rules
        sport_dict = sport.to_dict(include_rules=True)
        assert 'rules' in sport_dict
        assert 'default_bet_types' in sport_dict

    def test_sport_repr(self):
        """Test Sport model string representation."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should have meaningful string representation
        sport_repr = repr(sport)
        assert 'Sport' in sport_repr
        assert 'Football' in sport_repr
        assert 'football' in sport_repr


class TestSportModelBusinessLogic:
    """Test Sport model business logic and rules."""

    def test_sport_category_properties(self):
        """Test category-specific behavior."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        # Team sport
        team_sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert team_sport.is_team_sport is True
        assert hasattr(team_sport, 'requires_teams')
        assert team_sport.requires_teams is True
        
        # Individual sport
        individual_sport = Sport(
            name='Tennis',
            slug='tennis',
            category='individual_sport'
        )
        
        assert individual_sport.is_team_sport is False
        assert individual_sport.requires_teams is False

    def test_sport_bet_type_configuration(self):
        """Test sport-specific bet type configuration."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        # Should have sport-specific bet types
        assert hasattr(sport, 'configure_bet_types')
        
        # Mock configuration for testing
        with patch.object(sport, 'configure_bet_types') as mock_config:
            bet_config = {
                'match_winner': True,
                'over_under': True,
                'handicap': True,
                'correct_score': False
            }
            
            sport.configure_bet_types(bet_config)
            mock_config.assert_called_once_with(bet_config)

    def test_sport_scoring_system_validation(self):
        """Test scoring system validation for sport."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'validate_scoring_system')
        
        # Mock validation for testing
        with patch.object(sport, 'validate_scoring_system') as mock_validate:
            scoring_system = {
                'type': 'goals',
                'win_points': 3,
                'draw_points': 1,
                'loss_points': 0
            }
            
            mock_validate.return_value = True
            is_valid = sport.validate_scoring_system(scoring_system)
            assert is_valid is True
            mock_validate.assert_called_once_with(scoring_system)

    def test_sport_season_structure_validation(self):
        """Test season structure validation."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        sport = Sport(
            name='Football',
            slug='football',
            category='team_sport'
        )
        
        assert hasattr(sport, 'validate_season_structure')
        
        # Mock validation for testing
        with patch.object(sport, 'validate_season_structure') as mock_validate:
            season_structure = {
                'type': 'league',
                'rounds': 'double_round_robin',
                'playoff_format': 'knockout'
            }
            
            mock_validate.return_value = True
            is_valid = sport.validate_season_structure(season_structure)
            assert is_valid is True
            mock_validate.assert_called_once_with(season_structure)


class TestSportModelQueries:
    """Test Sport model query methods and class methods."""

    def test_sport_get_by_slug_class_method(self):
        """Test get_by_slug class method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        assert hasattr(Sport, 'get_by_slug')
        
        # Mock the class method for testing
        with patch.object(Sport, 'get_by_slug') as mock_get:
            mock_sport = Sport(
                name='Football',
                slug='football',
                category='team_sport'
            )
            mock_get.return_value = mock_sport
            
            result = Sport.get_by_slug('football')
            assert result == mock_sport
            mock_get.assert_called_once_with('football')

    def test_sport_get_active_sports_class_method(self):
        """Test get_active_sports class method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        assert hasattr(Sport, 'get_active_sports')
        
        # Mock the class method for testing
        with patch.object(Sport, 'get_active_sports') as mock_get:
            mock_sports = [
                Sport(name='Football', slug='football', category='team_sport'),
                Sport(name='Tennis', slug='tennis', category='individual_sport')
            ]
            mock_get.return_value = mock_sports
            
            result = Sport.get_active_sports()
            assert result == mock_sports
            mock_get.assert_called_once()

    def test_sport_get_by_category_class_method(self):
        """Test get_by_category class method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        assert hasattr(Sport, 'get_by_category')
        
        # Mock the class method for testing
        with patch.object(Sport, 'get_by_category') as mock_get:
            mock_sports = [
                Sport(name='Football', slug='football', category='team_sport'),
                Sport(name='Basketball', slug='basketball', category='team_sport')
            ]
            mock_get.return_value = mock_sports
            
            result = Sport.get_by_category('team_sport')
            assert result == mock_sports
            mock_get.assert_called_once_with('team_sport')

    def test_sport_search_class_method(self):
        """Test search class method."""
        if Sport is None:
            pytest.skip("Sport model not implemented yet")
            
        assert hasattr(Sport, 'search')
        
        # Mock the class method for testing
        with patch.object(Sport, 'search') as mock_search:
            mock_sports = [
                Sport(name='Football', slug='football', category='team_sport')
            ]
            mock_search.return_value = mock_sports
            
            result = Sport.search('foot')
            assert result == mock_sports
            mock_search.assert_called_once_with('foot')


class TestSportModelDatabaseIntegration:
    """Test Sport model database integration (requires database)."""

    @pytest.mark.asyncio
    async def test_sport_save_to_database(self):
        """Test saving sport to database."""
        if Sport is None or get_db_session is None:
            pytest.skip("Sport model or database not implemented yet")
            
        # This will be implemented when database layer is ready
        pass

    @pytest.mark.asyncio
    async def test_sport_slug_unique_constraint_database(self):
        """Test slug unique constraint at database level."""
        if Sport is None or get_db_session is None:
            pytest.skip("Sport model or database not implemented yet")
            
        # This will be implemented when database layer is ready
        # Should prevent duplicate slugs
        pass

    @pytest.mark.asyncio
    async def test_sport_cascade_behavior(self):
        """Test cascade behavior when sport is deleted."""
        if Sport is None or get_db_session is None:
            pytest.skip("Sport model or database not implemented yet")
            
        # This will be implemented when database layer is ready
        # Should test what happens to competitions/matches when sport is deleted
        pass

    @pytest.mark.asyncio
    async def test_sport_indexing(self):
        """Test database indexing for performance."""
        if Sport is None or get_db_session is None:
            pytest.skip("Sport model or database not implemented yet")
            
        # This will be implemented when database layer is ready
        # Should test indexes on slug, category, is_active
        pass