.DEFAULT_GOAL := help

APP ?= app
PORT ?= 8000

.PHONY: help run test lint fmt docker-up docker-down clean

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

run: ## Start the app (uvicorn for FastAPI, adjust as needed)
	uvicorn $(APP).main:app --reload --port $(PORT)

test: ## Run tests
	pytest -v

lint: ## Lint with ruff
	ruff check .
	mypy .

fmt: ## Format code
	ruff format .

docker-up: ## Start Docker services
	docker compose up -d

docker-down: ## Stop Docker services
	docker compose down

docker-logs: ## Tail Docker service logs
	docker compose logs -f

clean: ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete
	rm -rf dist/ build/ *.egg-info/
