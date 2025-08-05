# Use bash as the shell
SHELL := /bin/bash

# Define the Python interpreter and the Alembic command
VENV_PATH = venv
PYTHON = python3
ALEMBIC = alembic.config
COMMAND_UPGRADE = upgrade head

# Default target
initializeDatabase: install_venv, activate_venv, run_database_migrations, insert-data

install_venv:
	python3 -m venv .venv

activate_venv:
	source .venv/bin/activate

# Run the Alembic upgrade command
run_database_migrations:
	$(PYTHON) -m $(ALEMBIC) $(COMMAND_UPGRADE)


# Create basic data in docker database
insert-data:
	source venv/bin/activate && $(PYTHON) populate-database.py