"""Base model configuration for SQLAlchemy models."""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# This will be imported by all model files
__all__ = ["Base"]