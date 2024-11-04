# Makefile

# Default target
all:
	@echo "Available commands:"
	@echo "  make init                             - Initialize uv environment"
	@echo "  make github-init REPO=name            - Create GitHub repo and push code"
	@echo "  make new-page ROUTE=path/to/your/page  - Create a new page"
	@echo "  make migrations                        - Generate a new database migration"
	@echo "  make migrate                           - Apply database migrations"
	@echo "  make run                              - Run the FastHTML application"
	@echo "  make test                             - Run all tests"
	@echo "  make test-auth                        - Run auth tests only"
	@echo "  make test-coverage                    - Run tests with coverage report"
	@echo ""
	@echo "Example: make new-page ROUTE=users/[id]/profile"

# Command to create a new page
new-page:
	@if [ -z "$(ROUTE)" ]; then \
		echo "Error: ROUTE is not set. Usage: make new-page ROUTE=path/to/your/page"; \
		exit 1; \
	fi
	@python scripts/create_page.py $(ROUTE)

# Generate database migrations
migrations:
	alembic revision --autogenerate -m "initial"

# Apply database migrations
migrate:
	alembic upgrade head

# Run the FastHTML application
run:
	python project/main.py

# Run all tests
test:
	pytest project/tests/ -v

# Run tests with coverage report
test-coverage:
	pytest project/tests/ --cov=app --cov-report=html --cov-report=term-missing

# Initialize uv environment and activate it
init:
	@echo "Checking if uv is installed..."
	@if command -v uv >/dev/null 2>&1; then \
		echo "Creating new uv environment..."; \
		uv sync; \
		echo "Installing dependencies from pyproject.toml..."; \
		. .venv/bin/activate; \
		echo "Environment created and activated. Dependencies installed."; \
	else \
		echo "uv is not installed. Would you like to:"; \
		echo "1) Install uv (recommended)"; \
		echo "2) Continue with standard venv"; \
		read -p "Enter choice (1/2): " choice; \
		if [ "$$choice" = "1" ]; then \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
			echo "uv installed. Creating new environment..."; \
			uv venv .venv; \
			. .venv/bin/activate && uv pip install -e .; \
		else \
			echo "Creating standard venv environment..."; \
			python -m venv .venv; \
			. .venv/bin/activate && pip install -e .; \
			source .venv/bin/activate; \
		fi; \
	fi

# Clean up cache and coverage files
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage
	find . -type d -name "__pycache__" -exec rm -r {} +
	rm -rf .venv  # Added .venv cleanup

# Initialize and push to GitHub
github-init:
	@if not defined REPO ( \
		echo Error: REPO is not set. Usage: make github-init REPO=repository-name && \
		exit /b 1 \
	)
	@if not exist .git\ ( \
		echo Initializing Git repository... && \
		git init \
	) else ( \
		echo Git repository already initialized, continuing... \
	)
	@git add .
	@git commit -m "Initial commit" || ver > nul
	@echo "Checking current branch name..."
	@for /f "tokens=* USEBACKQ" %%F in (`git rev-parse --abbrev-ref HEAD`) do @( \
		if not "%%F"=="main" ( \
			echo Current branch is %%F, renaming to main... && \
			git branch -M main \
		) \
	)
	@echo "Checking if GitHub CLI is installed..."
	@where gh >nul 2>&1 && ( \
		echo Creating GitHub repository... && \
		"C:\Program Files\GitHub CLI\gh.exe" repo create $(REPO) --private --source=. --remote=origin || ver > nul \
	) || ( \
		echo "GitHub CLI (gh) is not installed. Skipping repository creation..." \
	)
	@echo Pushing to GitHub...
	@git push -u origin main
	@echo Repository successfully pushed to GitHub!

# Declare phony targets
.PHONY: all new-page migrations migrate run test test-auth test-coverage clean init github-init
