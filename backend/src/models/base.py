"""Base model configuration for SQLAlchemy models."""

from src.database import Base

# Re-export the Base from database module to maintain import consistency
__all__ = ["Base"]
