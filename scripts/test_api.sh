#!/bin/bash

# Sentiment Analysis API Test Script

set -e

API_URL="${API_URL:-http://localhost:8000}"
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}================================${NC}"
echo -e "${BLUE}Sentiment Analysis API Test${NC}"
echo -e "${BLUE}================================${NC}"
echo ""

# Check if API is running
echo -e "${BLUE}1. Checking API health...${NC}"
HEALTH=$(curl -s -o /dev/null -w "%{http_code}" $API_URL/health)
if [ $HEALTH -eq 200 ]; then
    echo -e "${GREEN}✓ API is healthy${NC}"
else
    echo -e "${RED}✗ API is not responding (HTTP $HEALTH)${NC}"
    exit 1
fi
echo ""

# Test positive sentiment
echo -e "${BLUE}2. Testing positive sentiment...${NC}"
echo "   Text: 'I love this product! It's amazing!'"
RESPONSE=$(curl -s -X POST "$API_URL/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product! It'\''s amazing!"}')
echo "   Response: $RESPONSE"
SENTIMENT=$(echo $RESPONSE | grep -o '"sentiment":"[^"]*"' | cut -d'"' -f4)
if [ "$SENTIMENT" = "positive" ]; then
    echo -e "   ${GREEN}✓ Correctly identified as positive${NC}"
else
    echo -e "   ${RED}✗ Expected positive, got $SENTIMENT${NC}"
fi
echo ""

# Test negative sentiment
echo -e "${BLUE}3. Testing negative sentiment...${NC}"
echo "   Text: 'This is terrible. I'm very disappointed.'"
RESPONSE=$(curl -s -X POST "$API_URL/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is terrible. I'\''m very disappointed."}')
echo "   Response: $RESPONSE"
SENTIMENT=$(echo $RESPONSE | grep -o '"sentiment":"[^"]*"' | cut -d'"' -f4)
if [ "$SENTIMENT" = "negative" ]; then
    echo -e "   ${GREEN}✓ Correctly identified as negative${NC}"
else
    echo -e "   ${RED}✗ Expected negative, got $SENTIMENT${NC}"
fi
echo ""

# Test neutral sentiment
echo -e "${BLUE}4. Testing neutral sentiment...${NC}"
echo "   Text: 'The weather is okay today.'"
RESPONSE=$(curl -s -X POST "$API_URL/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "The weather is okay today."}')
echo "   Response: $RESPONSE"
SENTIMENT=$(echo $RESPONSE | grep -o '"sentiment":"[^"]*"' | cut -d'"' -f4)
echo -e "   ${GREEN}✓ Got sentiment: $SENTIMENT${NC}"
echo ""

# Test cache statistics
echo -e "${BLUE}5. Checking cache statistics...${NC}"
CACHE_STATS=$(curl -s "$API_URL/cache/stats")
echo "   Cache stats: $CACHE_STATS"
echo -e "   ${GREEN}✓ Cache stats retrieved${NC}"
echo ""

# Test invalid input
echo -e "${BLUE}6. Testing error handling (empty text)...${NC}"
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$API_URL/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": ""}')
if [ $HTTP_CODE -eq 422 ]; then
    echo -e "   ${GREEN}✓ Correctly rejected empty text (HTTP $HTTP_CODE)${NC}"
else
    echo -e "   ${RED}✗ Expected HTTP 422, got $HTTP_CODE${NC}"
fi
echo ""

echo -e "${BLUE}================================${NC}"
echo -e "${GREEN}All tests completed!${NC}"
echo -e "${BLUE}================================${NC}"
echo ""
echo "To view API documentation, visit:"
echo "  • Swagger UI: $API_URL/docs"
echo "  • ReDoc: $API_URL/redoc"
echo ""