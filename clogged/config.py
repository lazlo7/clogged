from starlette.config import Config


# TODO: probably would be better to encapsulate this all under pydantic settings.
config = Config(".env")

APP_API_PORT      = config("APP_API_PORT", cast=int, default=8000)
ADMIN_API_KEY     = config("ADMIN_API_KEY", cast=str, default="sup3rs3cr3tk3y")
POSTGRES_HOST     = config("POSTGRES_HOST", cast=str, default="localhost")
POSTGRES_PORT     = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_USER     = config("POSTGRES_USER", cast=str, default="pastor")
POSTGRES_DB       = config("POSTGRES_DB", cast=str, default="pastor")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default="YOUR_DATABASE_PASSWORD")

# Providing an explicit way to set database dsn for an easy override.
DATABASE_DSN = config(
    "DATABASE_DSN", 
    cast=str, 
    default="postgresql://{user}:{password}@{host}:{port}/{name}".format(
        user=POSTGRES_USER, 
        password=POSTGRES_PASSWORD, 
        host=POSTGRES_HOST, 
        port=POSTGRES_PORT, 
        name=POSTGRES_DB
    )
)

# For easy ovveride as well.
DATABASE_ASYNCPG_DSN = config(
    "DATABASE_ASYNCPG_DSN", 
    cast=str, 
    default="postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
        user=POSTGRES_USER, 
        password=POSTGRES_PASSWORD, 
        host=POSTGRES_HOST, 
        port=POSTGRES_PORT, 
        name=POSTGRES_DB
    )
)

