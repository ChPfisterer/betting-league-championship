"""
Player model - minimal implementation for Team model dependencies.

This is a minimal implementation to support Team model testing.
Full implementation will be added in future TDD iterations.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

from .base import Base


class Player(Base):
    """Minimal Player model for Team dependencies."""
    
    __tablename__ = 'players'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    team_id = Column(UUID(as_uuid=True), ForeignKey('teams.id'))
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self) -> str:
        return f"<Player(id={self.id}, name='{self.name}')>"