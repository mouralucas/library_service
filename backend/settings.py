from rolf_common.backend.settings import Settings


class LibrarySettings(Settings):
    # Database and test settings
    library_database_url: str = (
        "postgresql+asyncpg://dev-user:password@localhost:5432/library_dev_db"
    )
    test_database_url: str = "sqlite+aiosqlite:///:memory:"
    echo_sql: bool = False
    echo_test_sql: bool = False
    test: bool = False

    # Project description
    project_name: str = "library"
    project_title: str = "Library Service Microservice"
    project_description: str = (
        "This service contains all necessary functions to manage a library"
    )
    project_version: str = "0.0.1"

    # Allowed origins CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:80,http://localhost"

    # Secrets settings
    jwt_token_secret: str = "my_dev_secret"

    # Server and Gateway
    eureka_host_name: str = "http://localhost:8761/eureka"

    library_host_ip: str = "192.168.0.29"
    library_host_port: int = 8001

    log_database_name: str = "library_dev_log"
    log_collection_name: str = "library_logs"
    log_database_url: str = (
        "mongodb://dev-user-logs:password@localhost:27017/library_dev_log?authSource=admin"
    )


settings = LibrarySettings()
