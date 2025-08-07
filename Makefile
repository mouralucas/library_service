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


run_database_migrations:
	$(PYTHON) -m $(ALEMBIC) $(COMMAND_UPGRADE)


insert_data:
	$(PYTHON) populate-database.py
