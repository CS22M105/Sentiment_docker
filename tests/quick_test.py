"""
Quick test script for the Sentiment Analysis API
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_api():
    print("=" * 60)
    print("Testing Sentiment Analysis API")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n1. Health Check...")
    response = requests.get(f"{API_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {json.dumps(response.json(), indent=2)}")
    
    # Test 2: Positive Sentiment
    print("\n2. Testing Positive Sentiment...")
    text = "I love this product! It's amazing!"
    response = requests.post(
        f"{API_URL}/analyze-sentiment",
        json={"text": text}
    )
    result = response.json()
    print(f"   Text: {text}")
    print(f"   Sentiment: {result['sentiment']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Explanation: {result['explanation']}")
    
    # Test 3: Negative Sentiment
    print("\n3. Testing Negative Sentiment...")
    text = "This is terrible. I'm very disappointed."
    response = requests.post(
        f"{API_URL}/analyze-sentiment",
        json={"text": text}
    )
    result = response.json()
    print(f"   Text: {text}")
    print(f"   Sentiment: {result['sentiment']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Explanation: {result['explanation']}")
    
    # Test 4: Neutral Sentiment
    print("\n4. Testing Neutral Sentiment...")
    text = "The weather is okay today."
    response = requests.post(
        f"{API_URL}/analyze-sentiment",
        json={"text": text}
    )
    result = response.json()
    print(f"   Text: {text}")
    print(f"   Sentiment: {result['sentiment']}")
    print(f"   Confidence: {result['confidence']:.2f}")
    print(f"   Explanation: {result['explanation']}")
    
    # Test 5: Cache Stats
    print("\n5. Cache Statistics...")
    response = requests.get(f"{API_URL}/cache/stats")
    print(f"   Cache stats: {json.dumps(response.json(), indent=2)}")
    
    print("\n" + "=" * 60)
    print("All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to API at", API_URL)
        print("   Make sure the API is running:")
        print("   - Docker: docker-compose up")
        print("   - Local: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")