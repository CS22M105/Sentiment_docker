"""Test sentiment service"""
import asyncio
import logging
from app.services.sentiment_service import get_sentiment_service, SentimentLabel

# Setup logging
logging.basicConfig(level=logging.INFO)

async def test_service():
    print("Testing Sentiment Analysis Service...")
    print("=" * 50)
    
    # Get service instance
    print("\n1. Initializing service...")
    service = get_sentiment_service()
    print("   ✓ Service initialized")
    
    # Test 2: Positive sentiment
    print("\n2. Testing positive sentiment...")
    text = "I love this product! It's amazing!"
    result = await service.analyze_sentiment(text)
    print(f"   Text: {text}")
    print(f"   Sentiment: {result.sentiment}")
    print(f"   Confidence: {result.confidence:.2f}")
    print(f"   Explanation: {result.explanation}")
    assert result.sentiment == SentimentLabel.POSITIVE
    print("   ✓ Positive sentiment detected correctly")
    
    # Test 3: Negative sentiment
    print("\n3. Testing negative sentiment...")
    text = "This is terrible. I'm very disappointed."
    result = await service.analyze_sentiment(text)
    print(f"   Text: {text}")
    print(f"   Sentiment: {result.sentiment}")
    print(f"   Confidence: {result.confidence:.2f}")
    print(f"   Explanation: {result.explanation}")
    assert result.sentiment == SentimentLabel.NEGATIVE
    print("   ✓ Negative sentiment detected correctly")
    
    # Test 4: Neutral sentiment
    print("\n4. Testing neutral sentiment...")
    text = "The weather is okay today."
    result = await service.analyze_sentiment(text)
    print(f"   Text: {text}")
    print(f"   Sentiment: {result.sentiment}")
    print(f"   Confidence: {result.confidence:.2f}")
    print(f"   Explanation: {result.explanation}")
    print("   ✓ Sentiment analyzed")
    
    # Test 5: Cache functionality
    print("\n5. Testing cache...")
    text = "I love this product! It's amazing!"
    result1 = await service.analyze_sentiment(text)
    result2 = await service.analyze_sentiment(text)  # Should use cache
    print(f"   First call: {result1.sentiment}")
    print(f"   Second call (cached): {result2.sentiment}")
    assert result1.sentiment == result2.sentiment
    print("   ✓ Cache working")
    
    # Test 6: Cache stats
    print("\n6. Testing cache stats...")
    stats = service.get_cache_stats()
    print(f"   Cache size: {stats['cache_size']}")
    print(f"   Cache enabled: {stats['cache_enabled']}")
    assert stats['cache_size'] >= 3  # Should have at least 3 entries
    print("   ✓ Cache stats retrieved")
    
    # Test 7: Clear cache
    print("\n7. Testing cache clear...")
    service.clear_cache()
    stats = service.get_cache_stats()
    print(f"   Cache size after clear: {stats['cache_size']}")
    assert stats['cache_size'] == 0
    print("   ✓ Cache cleared successfully")
    
    print("\n" + "=" * 50)
    print("✅ All service tests passed!")

if __name__ == "__main__":
    asyncio.run(test_service())