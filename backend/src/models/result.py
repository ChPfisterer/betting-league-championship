"""
Result model - minimal implementation for Match model dependencies.

This is a minimal implementation to support Match model testing.
Full implementation will be added in future TDD iterations.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

from .base import Base


class Result(Base):
    """Minimal Result model for Match dependencies."""
    
    __tablename__ = 'results'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    outcome = Column(String(20), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self) -> str:
        return f"<Result(id={self.id})>"