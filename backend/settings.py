from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database and test settings
    database_url: str  # Expected string in env 'postgresql+asyncpg://username:password@host_name:port/db_name'
    test_database_url: str
    echo_sql: bool = False
    echo_test_sql: bool = True
    test: bool = False

    # Project description
    project_name: str = "Library Service Microservice"
    project_description: str = "This service contains all necessary functions to manage a library"
    project_version: str = "0.0.1"

    # Secrets settings
    jwt_token_secret: str = "my_dev_secret"


settings = Settings()
