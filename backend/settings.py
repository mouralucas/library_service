from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database and test settings
    library_database_url: str = 'postgresql+asyncpg://dev-user:password@localhost:5432/library_dev_db'
    test_database_url: str = 'sqlite+aiosqlite:///:memory:'
    echo_sql: bool = False
    echo_test_sql: bool = True
    test: bool = False

    # Project description
    project_name: str = 'library-service'
    project_title: str = "Library Service Microservice"
    project_description: str = "This service contains all necessary functions to manage a library"
    project_version: str = "0.0.1"

    # Secrets settings
    jwt_token_secret: str = "my_dev_secret"

    # Server and Gateway
    eureka_host_name: str = 'http://localhost:8761/eureka'
    library_host_ip: str = '127.0.0.1'
    library_host_port: int = 8001

settings = Settings()
