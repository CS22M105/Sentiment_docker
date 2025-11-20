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

## Verification Checklist
- [ ] All files created in correct directories
- [ ] .env file has valid OPENAI_API_KEY
- [ ] Dependencies installed
- [ ] API starts without errors
- [ ] Health check returns 200: http://localhost:8000/health
- [ ] Swagger docs accessible: http://localhost:8000/docs
- [ ] Can analyze sentiment successfully

## Common Issues

**Issue: ModuleNotFoundError**
- Make sure all __init__.py files exist
- Check you're running from project root

**Issue: OPENAI_API_KEY not found**
- Verify .env file exists in project root
- Check API key is correctly set in .env

**Issue: Port 8000 already in use**
- Change port: `uvicorn app.main:app --port 8001`
- Or in docker-compose.yml: `"8001:8000"`

## Next Steps
1. Read the full README.md
2. Explore API docs at /docs
3. Try different test cases
4. Customize configuration in .env
```

---

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