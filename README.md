# Library Service

This service contains all necessary endpoints to handle library requests,
such as create a new item, add and author, publisher, new reading and reading progress, etc.

## Installation for development

There are two ways to run this project. The first is using Docker. 
There is a simple Dockerfile in the project that builds and runs the project.

```bash
docker run 
```

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
