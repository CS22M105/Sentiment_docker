# Step-by-Step Setup Instructions

## Prerequisites
- Python 3.11+ OR Docker
- OpenAI API Key

## Setup Steps

### Step 1: Create Project Structure
```bash
# Create project directory
mkdir sentiment-analysis-api
cd sentiment-analysis-api

# Create subdirectories
mkdir -p app/api app/services app/utils tests scripts
```

### Step 2: Create All __init__.py Files
```bash
# Create package init files
touch app/__init__.py
touch app/api/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py
```

### Step 3: Copy All Python Files
Copy these files to their respective locations:

**app/ directory:**
- `main.py`
- `config.py`
- `models.py`

**app/api/ directory:**
- `routes.py`

**app/services/ directory:**
- `sentiment_service.py`

**app/utils/ directory:**
- `logger.py`

**tests/ directory:**
- `test_api.py`

### Step 4: Copy Configuration Files
Copy to project root:
- `requirements.txt`
- `.env.example`
- `.gitignore`
- `Dockerfile`
- `docker-compose.yml`
- `Makefile`

### Step 5: Create .env File
```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### Step 6: Choose Setup Method

#### Option A: Docker (Recommended)
```bash
# Build and run
docker-compose up --build

# API will be available at http://localhost:8000
```

#### Option B: Local Development
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the API
uvicorn app.main:app --reload

# API will be available at http://localhost:8000
```

### Step 7: Test the API

**Option 1: Browser**
- Open http://localhost:8000/docs

**Option 2: cURL**
```bash
curl -X POST "http://localhost:8000/analyze-sentiment" \
  -H "Content-Type: application/json" \
  -d '{"text": "I love this product!"}'
```

**Option 3: Test Script**
```bash
chmod +x scripts/test_api.sh
./scripts/test_api.sh
```

**Option 4: Python Script**
```bash
python quick_test.py
```

### Step 8: Run Tests (Optional)
```bash
# Run pytest
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=app --cov-report=html
```

## Test the api working in terminal on user input
python test_user_input.py

## Complete File Tree

Your final project structure should look like this:
```
sentiment-analysis-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── sentiment_service.py
│   └── utils/
│       ├── __init__.py
│       └── logger.py
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── scripts/
│   └── test_api.sh
├── .env.example
├── .env (create this with your API key)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt
├── quick_test.py
├── setup_project.sh
└── SETUP_STEPS.md

# Additional files

 All these files do the testing on independent working of files.

### Test 1

python test_config.py
```

**Expected Output:**
```
Testing Configuration...
==================================================
✓ App Name: Sentiment Analysis API
✓ Version: 1.0.0
✓ Environment: development
✓ Log Level: INFO
✓ Model: gpt-4o-mini
✓ Temperature: 0.3
✓ Max Tokens: 150
✓ Cache Enabled: True
✓ Allowed Origins: ['http://localhost:3000', 'http://localhost:8000']
✓ API Key: sk-proj-xx...xxxx
✓ Is Development: True
✓ Is Production: False
==================================================
✅ Configuration test passed!

### Test 2

python test_models.py
```

**Expected Output:**
```
Testing Pydantic Models...
==================================================

1. Testing SentimentLabel...
   ✓ SentimentLabel enum works

2. Testing valid SentimentRequest...
   ✓ Valid request created

3. Testing whitespace stripping...
   ✓ Whitespace stripped correctly

4. Testing empty text validation...
   ✓ Empty text rejected correctly

5. Testing whitespace-only text...
   ✓ Whitespace-only text rejected correctly

6. Testing text length limit...
   ✓ Text length limit enforced

7. Testing SentimentResponse...
   ✓ SentimentResponse created successfully

8. Testing HealthResponse...
   ✓ HealthResponse created successfully

9. Testing ErrorResponse...
   ✓ ErrorResponse created successfully

==================================================
✅ All model tests passed!

### Test 3: LangChain

python test_service.py
```

**Expected Output:**
```
Testing Sentiment Analysis Service...
==================================================

1. Initializing service...
   ✓ Service initialized

2. Testing positive sentiment...
   Text: I love this product! It's amazing!
   Sentiment: positive
   Confidence: 0.95
   Explanation: The text expresses strong positive emotions...
   ✓ Positive sentiment detected correctly

3. Testing negative sentiment...
   Text: This is terrible. I'm very disappointed.
   Sentiment: negative
   Confidence: 0.92
   Explanation: The text contains negative words...
   ✓ Negative sentiment detected correctly

4. Testing neutral sentiment...
   Text: The weather is okay today.
   Sentiment: neutral
   Confidence: 0.75
   Explanation: The text has a neutral tone...
   ✓ Sentiment analyzed

5. Testing cache...
   First call: positive
   Second call (cached): positive
   ✓ Cache working

6. Testing cache stats...
   Cache size: 3
   Cache enabled: True
   ✓ Cache stats retrieved

7. Testing cache clear...
   Cache size after clear: 0
   ✓ Cache cleared successfully

==================================================
✅ All service tests passed!

### Test 4

python test_routes.py
```

**Expected Output:**
```
Testing API Routes...
==================================================

1. Testing health check...
   Status: healthy
   Version: 1.0.0
   Environment: development
   ✓ Health check working

2. Testing cache stats...
   Cache stats: {'cache_size': 0, 'cache_enabled': True}
   ✓ Cache stats endpoint working

==================================================
✅ All route tests passed!
