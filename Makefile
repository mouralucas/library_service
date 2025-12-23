SHELL := /bin/bash

# ===== Configuração base =====
VENV_PATH := .venv
PYTHON := $(VENV_PATH)/bin/python

ALEMBIC_MODULE := alembic.config
ALEMBIC_UPGRADE := upgrade head

# ===== Targets padrão =====
.DEFAULT_GOAL := help

help:
	@echo "Targets disponíveis:"
	@echo "  apply-migrations        Aplica migrations Alembic"
	@echo "  create-db-migration     Cria migration Alembic (autogenerate)"
	@echo "  insert-data             Popula banco com dados iniciais"
	@echo "  run-script              Executa script Python como módulo"

# ===== Banco / Alembic =====
apply-migrations:
	$(PYTHON) -m $(ALEMBIC_MODULE) $(ALEMBIC_UPGRADE)

create-db-migration:
	@read -p "Type the migration message: " msg; \
	$(PYTHON) -m $(ALEMBIC_MODULE) revision --autogenerate -m "$$msg"

# ===== Scripts =====
insert-data:
	$(PYTHON) -m populate_database

run-script:
	@if [ -z "$(script)" ]; then \
		echo "Uso: make run-script script=scripts.migrate_items_v2"; \
		exit 1; \
	fi
	$(PYTHON) -m $(script)

# ===== Qualidade =====
lint-graphql:
	npx graphql-schema-linter 'schemas_graphql/**/*.graphql'
