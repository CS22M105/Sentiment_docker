"""
Pydantic models for request/response validation.
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class SentimentLabel(str, Enum):
    """Enum for sentiment labels."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


class SentimentRequest(BaseModel):
    """Request model for sentiment analysis."""
    
    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to analyze for sentiment",
        examples=["I love this product! It's amazing!"]
    )
    
    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        """Validate and clean input text."""
        # Strip whitespace
        v = v.strip()
        
        # Check if empty after stripping
        if not v:
            raise ValueError("Text cannot be empty or only whitespace")
        
        return v
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "I love this product! It's amazing!"
                },
                {
                    "text": "This is terrible. I'm very disappointed."
                },
                {
                    "text": "The weather is okay today."
                }
            ]
        }
    }


class SentimentResponse(BaseModel):
    """Response model for sentiment analysis."""
    
    sentiment: SentimentLabel = Field(
        ...,
        description="The detected sentiment: positive, negative, or neutral"
    )
    
    confidence: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence score for the sentiment prediction (0-1)"
    )
    
    explanation: str = Field(
        ...,
        description="Brief explanation of why this sentiment was detected"
    )
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "sentiment": "positive",
                    "confidence": 0.95,
                    "explanation": "The text expresses strong positive emotions with words like 'love' and 'amazing'."
                }
            ]
        }
    }


class HealthResponse(BaseModel):
    """Response model for health check."""
    
    status: str = Field(default="healthy")
    version: str
    environment: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "healthy",
                    "version": "1.0.0",
                    "environment": "production"
                }
            ]
        }
    }


class ErrorResponse(BaseModel):
    """Response model for errors."""
    
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional error details")
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "error": "ValidationError",
                    "message": "Invalid input provided",
                    "detail": "Text cannot be empty"
                }
            ]
        }
    }