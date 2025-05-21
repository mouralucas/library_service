# Library Service

This service contains all necessary endpoints to handle library requests,
such as create a new item, add and author, publisher, new reading and reading progress, etc.

## Installation for development

There are two ways to run this project. 

```bash
sudo docker compose build
```

```bash
sudo docker compose up
```

This two commands will create the development database and run the project in port 8001.

First step is to create a new virtual environment. There are many ways to do that, 
but the simpler ways is to execute the following command:

```bash
python3 -m venv venv
```

This line will create a virtual environment called venv using the command venv from Python.

Than activate the venv.

```bash
sorce venv/bin/activate
```

To complete the configuration, install all requirements:

```bash
pip3 install -r requirements
```

## Run and debug in VSCode

If not exist, create a .vscode folder and a launch.json file with the following content:

```json
{
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Develop",
        "type": "debugpy",
        "request": "launch",
        "module": "uvicorn",
        "args": [
          "main:app",
          "--host", "127.0.0.1",
          "--port", "8000"
        ],
        "env": {
          "auth_service_base_url": "<auth_service_url>",
        },
        "jinja": true,
        "justMyCode": true,
        "console": "integratedTerminal"
      },
      {
        "name": "Production",
        "type": "debugpy",
        "request": "launch",
        "module": "uvicorn",
        "args": [
          "main:app",
          "--host", "127.0.0.1",
          "--port", "8000"
        ],
        "env": {
          "auth_service_base_url": "<auth_service_url>",
          "library_database_url": "<prod_database_connection>"
        },
        "jinja": true,
        "justMyCode": true,
        "console": "integratedTerminal"
      }
    ]
  }
```

The env `auth_service_base_url` is only needed when not running the user_server locally.
....

## Migrations

To run migrations, first create the file with the database changes:

```bash
python3 -m alembic.config revision --autogenerate -m [migration message]
```

Use a migration message that correspond with the changes in SQL models.

Finally, apply the changes into the database using:
```bash
python3 -m alembic.config upgrade head
```
