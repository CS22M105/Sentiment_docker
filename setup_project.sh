#!/bin/bash

# Setup script for Sentiment Analysis API
echo "Setting up Sentiment Analysis API project structure..."

# Create main directories
mkdir -p app/api app/services app/utils tests scripts

# Create __init__.py files
touch app/__init__.py
touch app/api/__init__.py
touch app/services/__init__.py
touch app/utils/__init__.py
touch tests/__init__.py

# Create empty .env file (will need to add API key)
touch .env

echo "✅ Directory structure created!"
echo ""
echo "Next steps:"
echo "1. Copy all .py files to their respective directories"
echo "2. Copy .env.example, requirements.txt, Dockerfile, docker-compose.yml to root"
echo "3. Add your OPENAI_API_KEY to .env file"
echo "4. Run: pip install -r requirements.txt"
echo "5. Run: uvicorn app.main:app --reload"