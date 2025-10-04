"""
Match model - minimal implementation for Sport model dependencies.

This is a minimal implementation to support Sport model testing.
Full implementation will be added in future TDD iterations.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

from .base import Base


class Match(Base):
    """Minimal Match model for Sport dependencies."""
    
    __tablename__ = 'matches'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self) -> str:
        return f"<Match(id={self.id}, name='{self.name}')>"