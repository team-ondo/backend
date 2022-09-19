
.PHONY: run test require reset-table seed help

.DEFAULT_GOAL := help

run: ## Run server
	uvicorn src.main:app --reload --host 0.0.0.0

test: ## Run test
	pytest --color=yes --code-highlight=yes --no-header -v

require: ## Regenerate requirements.txt from pyproject.toml
	poetry export --without-hashes --with dev --output requirements.txt

reset-table: ## Recreate tables
	poetry run python -m src.migrate_db

seed: ## Seed data
	poetry run python -m src.seed_db

help: ## Show help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
