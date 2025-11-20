"""
Tests for the API endpoints.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestSentimentAPI:
    """Test cases for sentiment analysis endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "environment" in data
    
    def test_analyze_positive_sentiment(self):
        """Test analyzing positive sentiment."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "I love this product! It's amazing!"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "positive"
        assert "confidence" in data
        assert "explanation" in data
        assert 0 <= data["confidence"] <= 1
    
    def test_analyze_negative_sentiment(self):
        """Test analyzing negative sentiment."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "This is terrible. I'm very disappointed."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "negative"
        assert "confidence" in data
        assert "explanation" in data
    
    def test_analyze_neutral_sentiment(self):
        """Test analyzing neutral sentiment."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "The weather is okay today."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] in ["neutral", "positive", "negative"]
        assert "confidence" in data
        assert "explanation" in data
    
    def test_empty_text(self):
        """Test with empty text."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": ""}
        )
        assert response.status_code == 422
    
    def test_whitespace_only(self):
        """Test with whitespace-only text."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "   "}
        )
        assert response.status_code == 422
    
    def test_very_long_text(self):
        """Test with very long text."""
        long_text = "This is great! " * 500  # 7500+ characters
        response = client.post(
            "/analyze-sentiment",
            json={"text": long_text}
        )
        assert response.status_code == 422  # Exceeds 5000 char limit
    
    def test_missing_text_field(self):
        """Test with missing text field."""
        response = client.post("/analyze-sentiment", json={})
        assert response.status_code == 422
    
    def test_cache_stats(self):
        """Test cache statistics endpoint."""
        response = client.get("/cache/stats")
        assert response.status_code == 200
        data = response.json()
        assert "cache_size" in data
        assert "cache_enabled" in data
    
    def test_clear_cache(self):
        """Test cache clearing endpoint."""
        response = client.post("/cache/clear")
        assert response.status_code == 204
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert "docs" in data


class TestSentimentEdgeCases:
    """Test edge cases for sentiment analysis."""
    
    def test_mixed_sentiment(self):
        """Test text with mixed sentiments."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "The product is good but the price is terrible."}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] in ["positive", "negative", "neutral"]
    
    def test_sarcasm(self):
        """Test sarcastic text."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "Oh great, another delay. Just wonderful."}
        )
        assert response.status_code == 200
        # Sarcasm is hard, so we just check it returns valid response
        data = response.json()
        assert data["sentiment"] in ["positive", "negative", "neutral"]
    
    def test_emojis(self):
        """Test text with emojis."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "I love this! 😍🎉"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == "positive"
    
    def test_special_characters(self):
        """Test text with special characters."""
        response = client.post(
            "/analyze-sentiment",
            json={"text": "Great!!! Amazing... Really???"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "sentiment" in data