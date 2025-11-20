"""
API routes for sentiment analysis.
"""
import logging
from typing import Dict

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from app.models import (
    SentimentRequest,
    SentimentResponse,
    HealthResponse,
    ErrorResponse
)
from app.services.sentiment_service import get_sentiment_service
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/analyze-sentiment",
    response_model=SentimentResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {
            "description": "Successful sentiment analysis",
            "model": SentimentResponse
        },
        400: {
            "description": "Invalid input",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    },
    summary="Analyze text sentiment",
    description="Analyzes the sentiment of the provided text and returns positive, negative, or neutral classification with explanation."
)
async def analyze_sentiment(request: SentimentRequest) -> SentimentResponse:
    """
    Analyze the sentiment of the provided text.
    
    **Input:**
    - text: The text to analyze (1-5000 characters)
    
    **Output:**
    - sentiment: positive, negative, or neutral
    - confidence: confidence score (0-1)
    - explanation: brief explanation of the analysis
    
    **Example:**
```json
    {
        "text": "I love this product! It's amazing!"
    }
```
    
    **Response:**
```json
    {
        "sentiment": "positive",
        "confidence": 0.95,
        "explanation": "The text expresses strong positive emotions with words like 'love' and 'amazing'."
    }
```
    """
    try:
        logger.info(f"Received sentiment analysis request: {request.text[:50]}...")
        
        # Get sentiment service
        service = get_sentiment_service()
        
        # Analyze sentiment
        result = await service.analyze_sentiment(request.text)
        
        # Convert to response model
        response = SentimentResponse(
            sentiment=result.sentiment,
            confidence=result.confidence,
            explanation=result.explanation
        )
        
        logger.info(f"Sentiment analysis successful: {response.sentiment}")
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing sentiment analysis: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while analyzing sentiment"
        )


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is running and healthy"
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns the service status, version, and environment.
    """
    return HealthResponse(
        status="healthy",
        version=settings.app_version,
        environment=settings.environment
    )


@router.get(
    "/cache/stats",
    response_model=Dict[str, int],
    status_code=status.HTTP_200_OK,
    summary="Get cache statistics",
    description="Get current cache size and status"
)
async def get_cache_stats() -> Dict[str, int]:
    """
    Get cache statistics.
    
    Returns information about the current cache state.
    """
    service = get_sentiment_service()
    return service.get_cache_stats()


@router.post(
    "/cache/clear",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear cache",
    description="Clear the sentiment analysis cache"
)
async def clear_cache():
    """
    Clear the sentiment analysis cache.
    
    This will force all subsequent requests to be re-analyzed.
    """
    service = get_sentiment_service()
    service.clear_cache()
    logger.info("Cache cleared via API endpoint")
    return JSONResponse(
        status_code=status.HTTP_204_NO_CONTENT,
        content=None
    )