"""
Database dependency injection and session management.

This module provides FastAPI dependency injection for database sessions
and enhanced database utilities for the API layer.
"""

from contextlib import contextmanager
from typing import Generator

from fastapi import Depends, HTTPException, status
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from .config import get_settings

settings = get_settings()

# Create SQLAlchemy engine with settings
engine = create_engine(
    settings.database_url,
    echo=settings.database_echo,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections every 5 minutes
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session injection.
    
    Yields:
        Session: SQLAlchemy database session
        
    Raises:
        HTTPException: If database connection fails
    """
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database session outside of FastAPI.
    
    Yields:
        Session: SQLAlchemy database session
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def create_tables():
    """Create all database tables and apply schema updates."""
    # First, handle any schema migrations
    _migrate_schema()
    
    # Then create/update all tables
    Base.metadata.create_all(bind=engine)


def _migrate_schema():
    """Apply any necessary schema migrations."""
    try:
        with engine.connect() as conn:
            # Add keycloak_id column if it doesn't exist
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='keycloak_id'
            """))
            if not result.fetchone():
                # Add keycloak_id column
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN keycloak_id VARCHAR(255) UNIQUE
                """))
                conn.commit()
                print("✅ Added keycloak_id column to users table")
    except Exception as e:
        print(f"Note: Could not check/add keycloak_id column: {e}")


def drop_tables():
    """Drop all database tables."""
    Base.metadata.drop_all(bind=engine)


# Database session dependency
DatabaseSession = Depends(get_db)