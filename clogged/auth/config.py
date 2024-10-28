from pydantic_settings import BaseSettings


class AuthConfig(BaseSettings):
    # Session expires in 30 days.
    CLOGGED_SESSION_EXPIRES_IN_SECONDS: int = 60*60*24*30


settings = AuthConfig()
