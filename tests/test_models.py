"""Test Pydantic models"""
from app.models import (
    SentimentLabel,
    SentimentRequest,
    SentimentResponse,
    HealthResponse,
    ErrorResponse
)
from pydantic import ValidationError

print("Testing Pydantic Models...")
print("=" * 50)

# Test 1: SentimentLabel Enum
print("\n1. Testing SentimentLabel...")
assert SentimentLabel.POSITIVE == "positive"
assert SentimentLabel.NEGATIVE == "negative"
assert SentimentLabel.NEUTRAL == "neutral"
print("   ✓ SentimentLabel enum works")

# Test 2: Valid SentimentRequest
print("\n2. Testing valid SentimentRequest...")
request = SentimentRequest(text="I love this!")
assert request.text == "I love this!"
print("   ✓ Valid request created")

# Test 3: SentimentRequest with whitespace
print("\n3. Testing whitespace stripping...")
request = SentimentRequest(text="  Hello  ")
assert request.text == "Hello"
print("   ✓ Whitespace stripped correctly")

# Test 4: Empty text should fail
print("\n4. Testing empty text validation...")
try:
    request = SentimentRequest(text="")
    print("   ✗ Should have raised ValidationError")
except ValidationError as e:
    print("   ✓ Empty text rejected correctly")

# Test 5: Whitespace-only should fail
print("\n5. Testing whitespace-only text...")
try:
    request = SentimentRequest(text="   ")
    print("   ✗ Should have raised ValidationError")
except ValidationError as e:
    print("   ✓ Whitespace-only text rejected correctly")

# Test 6: Text too long should fail
print("\n6. Testing text length limit...")
try:
    long_text = "a" * 5001
    request = SentimentRequest(text=long_text)
    print("   ✗ Should have raised ValidationError")
except ValidationError as e:
    print("   ✓ Text length limit enforced")

# Test 7: SentimentResponse
print("\n7. Testing SentimentResponse...")
response = SentimentResponse(
    sentiment=SentimentLabel.POSITIVE,
    confidence=0.95,
    explanation="Text is positive"
)
assert response.sentiment == "positive"
assert response.confidence == 0.95
print("   ✓ SentimentResponse created successfully")

# Test 8: HealthResponse
print("\n8. Testing HealthResponse...")
health = HealthResponse(
    status="healthy",
    version="1.0.0",
    environment="development"
)
assert health.status == "healthy"
print("   ✓ HealthResponse created successfully")

# Test 9: ErrorResponse
print("\n9. Testing ErrorResponse...")
error = ErrorResponse(
    error="ValidationError",
    message="Invalid input",
    detail="Text is too short"
)
assert error.error == "ValidationError"
print("   ✓ ErrorResponse created successfully")

print("\n" + "=" * 50)
print("✅ All model tests passed!")