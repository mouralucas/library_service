# Library Service

Este serviço contem os endipoints necessarios para lidar com requests da biblioteca, como criar novos items, adicionar autores, editoras, leituras, etc.

## Instalação para desenvolvimento

Basta rodar o container:

```bash
sudo docker compose build
```

```bash
sudo docker compose up
```

Esses comandos criam um container Docker com o banco de dados de desenvolvimento roda o projeto na porta 8001

## Executar e debugar no VSCode

Caso não exista, crie a pasta .vscode na raiz do projeto e um arquivo launch.json com o seguinte código:

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

A variável `auth_service_base_url` somente é necessária quando rodar o serviço user_server localmente.
....

## Migrations

As migrações são utilizadas para a criação/edição das informações do banco de dados. Elas mapeiam os models do sql alchemy do projeto e aplicam no banco de dados

## Instalação do Alembic

Para inicializar o alembic basta rodar o seguinte comando:

```bash
alembic init alembic
``` 

Esse comando irá gerar os arquivos básicos do Alembic

```
alembic/
  env.py
  README
  script.py.mako
  versions/
alembic.ini
```

Para rodar as migrações, rode o comando 'revision' para que o Alembic identifique as modificações nos models e gere um arquivo de migração

```bash
python3 -m alembic.config revision --autogenerate -m [migration message]
```

Use mensagens que correnspondam com as mudanças aplicadas nos models.

Finalmente, aplique as modificações no banco de dados

```bash
python3 -m alembic.config upgrade head
```
