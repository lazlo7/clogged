from pydantic import Field, computed_field, PostgresDsn, RedisDsn
from pydantic_core import MultiHostUrl, Url
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    CLOGGED_API_PORT: int = 8000
    CLOGGED_IS_DEVELOPMENT: bool = False
    
    """Backing field, use `CLOGGED_ENABLE_API_DOCS` property instead."""
    clogged_enable_api_docs: bool = Field(default=False, alias="CLOGGED_ENABLE_API_DOCS")
    @property
    def CLOGGED_ENABLE_API_DOCS(self) -> bool:
        # Default to development mode if not specified.
        return self.CLOGGED_IS_DEVELOPMENT or self.clogged_enable_api_docs

    """Backing field, use `CLOGGED_CORS_ALLOW_ORIGINS` property instead."""
    clogged_cors_allowed_origins: str = Field(default="http://localhost", alias="CLOGGED_CORS_ALLOWED_ORIGINS")
    @property
    def CLOGGED_CORS_ALLOWED_ORIGINS(self) -> list[str]:
        # TODO: Add validation for the origins.
        return self.clogged_cors_allowed_origins.split(",")
    

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "clogged"
    POSTGRES_DB: str = "clogged"
    POSTGRES_PASSWORD: str = "sup3rs3cr3tpassw0rd"
    
    
    @computed_field
    @property
    def DATABASE_DSN(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+asyncpg",
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            path=self.POSTGRES_DB,
            password=self.POSTGRES_PASSWORD
        )
    

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: str = "0"

    
    @computed_field
    @property
    def REDIS_DSN(self) -> RedisDsn:
        return Url.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=self.REDIS_DB
        )


settings = Config()
