"""Test full application with HTTP client"""
import requests
import json

API_URL = "http://localhost:8000"

print("Testing Full Application...")
print("=" * 50)

# Test 1: Root endpoint
print("\n1. Testing root endpoint...")
response = requests.get(f"{API_URL}/")
assert response.status_code == 200
data = response.json()
print(f"   ✓ Root: {data['name']}")

# Test 2: Health check
print("\n2. Testing health endpoint...")
response = requests.get(f"{API_URL}/health")
assert response.status_code == 200
data = response.json()
print(f"   ✓ Status: {data['status']}")

# Test 3: Analyze positive sentiment
print("\n3. Testing positive sentiment...")
response = requests.post(
    f"{API_URL}/analyze-sentiment",
    json={"text": "I love this product!"}
)
assert response.status_code == 200
data = response.json()
print(f"   Sentiment: {data['sentiment']}")
print(f"   Confidence: {data['confidence']:.2f}")
print(f"   Explanation: {data['explanation']}")
assert data['sentiment'] == 'positive'
print("   ✓ Positive sentiment detected")

# Test 4: Analyze negative sentiment
print("\n4. Testing negative sentiment...")
response = requests.post(
    f"{API_URL}/analyze-sentiment",
    json={"text": "This is terrible!"}
)
assert response.status_code == 200
data = response.json()
print(f"   Sentiment: {data['sentiment']}")
assert data['sentiment'] == 'negative'
print("   ✓ Negative sentiment detected")

# Test 5: Invalid input (empty text)
print("\n5. Testing validation...")
response = requests.post(
    f"{API_URL}/analyze-sentiment",
    json={"text": ""}
)
assert response.status_code == 422
print("   ✓ Empty text rejected")

# Test 6: Cache stats
print("\n6. Testing cache stats...")
response = requests.get(f"{API_URL}/cache/stats")
assert response.status_code == 200
data = response.json()
print(f"   Cache size: {data['cache_size']}")
print("   ✓ Cache stats retrieved")

print("\n" + "=" * 50)
print("✅ Full application test passed!")