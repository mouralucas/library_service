# Define the Python interpreter and the Alembic command
PYTHON = python3
ALEMBIC = alembic.config
COMMAND_UPGRADE = upgrade head

# Default target
all: upgrade

# Run the Alembic auto

# Run the Alembic upgrade command
upgrade:
	$(PYTHON) -m $(ALEMBIC) $(COMMAND_UPGRADE)
