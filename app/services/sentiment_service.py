"""
Sentiment analysis service using LangChain.
"""
import json
import logging
from typing import Dict, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from app.config import settings
from app.models import SentimentLabel

logger = logging.getLogger(__name__)


class SentimentOutput(BaseModel):
    """Structured output for sentiment analysis."""
    sentiment: SentimentLabel = Field(description="The sentiment: positive, negative, or neutral")
    confidence: float = Field(description="Confidence score between 0 and 1", ge=0.0, le=1.0)
    explanation: str = Field(description="Brief explanation of the sentiment")


class SentimentAnalysisService:
    """
    Service for analyzing sentiment using LangChain and OpenAI.
    Implements caching, retry logic, and structured output.
    """
    
    def __init__(self):
        """Initialize the sentiment analysis service."""
        self.llm = self._initialize_llm()
        self.parser = PydanticOutputParser(pydantic_object=SentimentOutput)
        self.chain = self._create_chain()
        self._cache: Dict[str, SentimentOutput] = {}
        logger.info("Sentiment analysis service initialized")
    
    def _initialize_llm(self) -> ChatOpenAI:
        """Initialize the language model with configuration."""
        return ChatOpenAI(
            model=settings.model_name,
            temperature=settings.model_temperature,
            max_tokens=settings.max_tokens,
            api_key=settings.openai_api_key,
            max_retries=settings.max_retries,
            timeout=settings.timeout,
        )
    
    def _create_chain(self):
        """Create the LangChain sentiment analysis chain."""
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert sentiment analyzer. Analyze the sentiment of the given text 
            and respond with a JSON object containing:
            - sentiment: one of "positive", "negative", or "neutral"
            - confidence: a number between 0 and 1 indicating your confidence
            - explanation: a brief (1-2 sentences) explanation of your analysis
            
            Be precise and objective in your analysis. Consider:
            - Emotional tone and word choice
            - Context and implied meaning
            - Overall message and intent
            
            {format_instructions}"""),
            ("user", "Analyze the sentiment of this text: {text}")
        ])
        
        # Format the prompt with parser instructions
        formatted_prompt = prompt.partial(
            format_instructions=self.parser.get_format_instructions()
        )
        
        # Create the chain
        chain = formatted_prompt | self.llm | self.parser
        return chain
    
    def _get_cache_key(self, text: str) -> str:
        """Generate cache key from text."""
        return text.lower().strip()
    
    async def analyze_sentiment(
        self, 
        text: str, 
        use_cache: bool = True
    ) -> SentimentOutput:
        """
        Analyze the sentiment of the given text.
        
        Args:
            text: The text to analyze
            use_cache: Whether to use cached results
            
        Returns:
            SentimentOutput with sentiment, confidence, and explanation
            
        Raises:
            Exception: If analysis fails
        """
        # Check cache
        if use_cache and settings.enable_cache:
            cache_key = self._get_cache_key(text)
            if cache_key in self._cache:
                logger.info(f"Cache hit for text: {text[:50]}...")
                return self._cache[cache_key]
        
        try:
            logger.info(f"Analyzing sentiment for text: {text[:50]}...")
            
            # Invoke the chain
            result = await self.chain.ainvoke({"text": text})
            
            # Cache the result
            if settings.enable_cache:
                self._cache[cache_key] = result
            
            logger.info(
                f"Sentiment analysis complete: {result.sentiment} "
                f"(confidence: {result.confidence:.2f})"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}", exc_info=True)
            # Fallback to basic sentiment
            return await self._fallback_analysis(text, str(e))
    
    async def _fallback_analysis(self, text: str, error: str) -> SentimentOutput:
        """
        Provide a fallback sentiment analysis if LLM fails.
        Uses simple keyword matching.
        """
        logger.warning(f"Using fallback analysis due to error: {error}")
        
        text_lower = text.lower()
        
        # Simple keyword-based analysis
        positive_words = ["love", "great", "excellent", "amazing", "wonderful", "good", "best"]
        negative_words = ["hate", "terrible", "awful", "horrible", "worst", "bad", "disappointing"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = SentimentLabel.POSITIVE
            confidence = min(0.6, 0.4 + (positive_count * 0.1))
            explanation = f"Text contains {positive_count} positive keyword(s). (Fallback analysis)"
        elif negative_count > positive_count:
            sentiment = SentimentLabel.NEGATIVE
            confidence = min(0.6, 0.4 + (negative_count * 0.1))
            explanation = f"Text contains {negative_count} negative keyword(s). (Fallback analysis)"
        else:
            sentiment = SentimentLabel.NEUTRAL
            confidence = 0.5
            explanation = "No strong sentiment indicators detected. (Fallback analysis)"
        
        return SentimentOutput(
            sentiment=sentiment,
            confidence=confidence,
            explanation=explanation
        )
    
    def clear_cache(self):
        """Clear the sentiment analysis cache."""
        self._cache.clear()
        logger.info("Cache cleared")
    
    def get_cache_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        return {
            "cache_size": len(self._cache),
            "cache_enabled": settings.enable_cache
        }


# Global service instance
_service: Optional[SentimentAnalysisService] = None


def get_sentiment_service() -> SentimentAnalysisService:
    """
    Get or create the sentiment analysis service.
    Singleton pattern to reuse the LLM connection.
    """
    global _service
    if _service is None:
        _service = SentimentAnalysisService()
    return _service