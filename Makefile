.PHONY: help install dev test clean docker-build docker-run docker-stop format lint

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

dev: ## Run development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run tests
	pytest tests/ -v --cov=app --cov-report=html

test-api: ## Run API tests with script
	chmod +x scripts/test_api.sh
	./scripts/test_api.sh

clean: ## Clean cache and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .mypy_cache

docker-build: ## Build Docker image
	docker-compose build

docker-up: ## Start Docker containers
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

docker-logs: ## View Docker logs
	docker-compose logs -f

docker-shell: ## Open shell in container
	docker-compose exec sentiment-api bash

format: ## Format code with black and isort
	black app/ tests/
	isort app/ tests/

lint: ## Lint code with flake8
	flake8 app/ tests/ --max-line-length=100

setup: ## Initial project setup
	cp .env.example .env
	@echo "Please edit .env and add your OPENAI_API_KEY"

all: install format lint test ## Run all checks