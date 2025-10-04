"""Base model configuration for SQLAlchemy models."""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# This will be imported by all model files
__all__ = ["Base"]
