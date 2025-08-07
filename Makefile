# Use bash as the shell
SHELL := /bin/bash

# Configuração
VENV_PATH := .venv
PYTHON := $(VENV_PATH)/bin/python
ALEMBIC := alembic
COMMAND_UPGRADE := upgrade head

# Alvo padrão
initializeDatabase: check_venv run_database_migrations insert_data

# Verifica se a venv existe, se não, cria
check_venv:
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Criando virtualenv em $(VENV_PATH)"; \
		python3 -m venv $(VENV_PATH); \
	else \
		echo "Virtualenv já existe em $(VENV_PATH)"; \
	fi

# Roda as migrations com Alembic usando o python da venv
run_database_migrations:
	$(PYTHON) -m $(ALEMBIC) $(COMMAND_UPGRADE)

# Insere dados usando a venv
insert_data:
	$(PYTHON) populate-database.py
