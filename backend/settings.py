from pydantic import BaseModel, Field, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class DatabaseConfig(BaseModel):
    """Backend database configuration parameters.

    Attributes:
        dsn:
            DSN for target database.
    """
    dsn: str = Field(
        default="postgresql+asyncpg://user:password@host:port/dbname",
        env="MYAPI_DATABASE__DSN"
    )


class AppSettings(BaseSettings):
    name: str = 'Library service'
    description: str = 'This service contains all necessary functions to manage a library'
    version: str = '0.0.2'
    contact_email: str = 'lucaspenha471@gmail.com'
    license_url: AnyHttpUrl = "https://www.apache.org/licenses/LICENSE-2.0.html"


class Settings(BaseSettings):
    """API configuration parameters.

    Automatically read modifications to the configuration parameters
    from environment variables and ``.env`` file.

    Attributes:
        DATABASE:
            Database configuration settings.
            Instance of :class:`app.backend.config.DatabaseConfig`.
        token_key:
            Random secret key used to sign JWT tokens.
    """

    DATABASE: DatabaseConfig = DatabaseConfig()
    APP_SETTINGS: AppSettings = AppSettings()
    token_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="MYAPI_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )


# TODO: research lru caching with functools
@lru_cache
def get_settings() -> Settings:
    return Settings()
