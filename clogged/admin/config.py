from pydantic_settings import BaseSettings, SettingsConfigDict


class AdminConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    CLOGGED_ADMIN_API_KEY: str = "sup3rs3cr3tk3y"


settings = AdminConfig()
