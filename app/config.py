"""
Configuration management using Pydantic Settings.
Supports environment variables and .env files.
"""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with validation."""
    
    # API Configuration
    app_name: str = "Sentiment Analysis API"
    app_version: str = "1.0.0"
    environment: str = Field(default="development", pattern="^(development|staging|production)$")
    log_level: str = Field(default="INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    # OpenAI Configuration
    openai_api_key: str = Field(..., min_length=20)
    model_name: str = Field(default="gpt-4o-mini")
    model_temperature: float = Field(default=0.3, ge=0.0, le=2.0)
    max_tokens: int = Field(default=150, ge=50, le=500)
    
    # API Settings
    max_retries: int = Field(default=3, ge=1, le=10)
    timeout: int = Field(default=30, ge=10, le=120)
    rate_limit_requests: int = Field(default=100, ge=1)
    rate_limit_period: int = Field(default=60, ge=1)
    
    # CORS Settings
    allowed_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"]
    )
    
    # Cache Settings
    enable_cache: bool = Field(default=True)
    cache_ttl: int = Field(default=3600, ge=60)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Using lru_cache ensures we only create one instance.
    """
    return Settings()


# Global settings instance
settings = get_settings()