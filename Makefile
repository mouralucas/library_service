SHELL := /bin/bash


VENV_PATH := .venv
PYTHON := $(VENV_PATH)/bin/python
ALEMBIC := alembic
COMMAND_UPGRADE := upgrade head


initializeDatabase: check_venv run_database_migrations insert_data

check_venv:
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Criando virtualenv em $(VENV_PATH)"; \
		python3 -m venv $(VENV_PATH); \
	else \
		echo "Virtualenv já existe em $(VENV_PATH)"; \
	fi

build: 
	docker compose build

# Run the Alembic upgrade command
apply-migrations:
	$(PYTHON) -m $(ALEMBIC) $(COMMAND_UPGRADE)

create-migration:
	@read -p "Type the migration message: " msg; \
	python3 -m alembic.config revision --autogenerate -m "$$msg"


# Create basic data in docker database
insert-data:
	source venv/bin/activate && $(PYTHON) populate-database.py


# Lint GraphQL schema files (requires node/npm). Uses npx so installation isn't mandatory
lint-graphql:
	npx graphql-schema-linter 'schemas_graphql/**/*.graphql'
