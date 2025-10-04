"""
Season model - minimal implementation for Competition model dependencies.

This is a minimal implementation to support Competition model testing.
Full implementation will be added in future TDD iterations.
"""

from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime, timezone
import uuid

from .base import Base


class Season(Base):
    """Minimal Season model for Competition dependencies."""
    
    __tablename__ = 'seasons'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    def __repr__(self) -> str:
        return f"<Season(id={self.id}, name='{self.name}', year={self.year})>"