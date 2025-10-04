"""
Application configuration settings.

Centralized configuration management for the betting platform API
using Pydantic settings with environment variable support.
"""

from functools import lru_cache
from typing import List, Optional

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application
    app_name: str = "Multi-Sport Betting Platform API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/betting_league_championship"
    database_echo: bool = False
    
    # API
    api_v1_str: str = "/api/v1"
    
    # CORS
    backend_cors_origins: List[str] = [
        "http://localhost:4200",  # Angular dev server
        "http://localhost:3000",  # Alternative frontend
        "http://localhost:8080",  # Alternative frontend
    ]
    
    @field_validator("backend_cors_origins", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from environment variable or return list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Security
    secret_key: str = "your-secret-key-here-change-in-production"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Keycloak OAuth
    keycloak_server_url: Optional[str] = None
    keycloak_realm: str = "betting-platform"
    keycloak_client_id: str = "betting-api"
    keycloak_client_secret: Optional[str] = None
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        """Pydantic config for environment variables."""
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()


# Global settings instance
settings = get_settings()