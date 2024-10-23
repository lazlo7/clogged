from starlette.config import Config


# TODO: Decouple app settings and use pydantc's BaseSettings.
config = Config(".env")

APP_API_PORT      = config("APP_API_PORT", cast=int, default=8000)
ADMIN_API_KEY     = config("ADMIN_API_KEY", cast=str, default="sup3rs3cr3tk3y")
POSTGRES_HOST     = config("POSTGRES_HOST", cast=str, default="localhost")
POSTGRES_PORT     = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_USER     = config("POSTGRES_USER", cast=str, default="clogged")
POSTGRES_DB       = config("POSTGRES_DB", cast=str, default="clogged")
POSTGRES_PASSWORD = config("POSTGRES_PASSWORD", cast=str, default="YOUR_DATABASE_PASSWORD")

# Providing an explicit way to set database dsn for an easy override.
DATABASE_DSN = config(
    "DATABASE_DSN", 
    cast=str, 
    default="postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}".format(
        user=POSTGRES_USER, 
        password=POSTGRES_PASSWORD, 
        host=POSTGRES_HOST, 
        port=POSTGRES_PORT, 
        name=POSTGRES_DB
    )
)

REDIS_HOST = config("REDIS_HOST", cast=str, default="localhost")
REDIS_PORT = config("REDIS_PORT", cast=int, default=6379)
REDIS_DB   = config("REDIS_DB", cast=int, default=0)

REDIS_DSN = config(
    "REDIS_DSN", 
    cast=str, 
    default="redis://{host}:{port}/{db}".format(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        db=REDIS_DB
    )
)

# Session expires in 30 days.
SESSION_EXPIRES_IN_SECONDS = config("SESSION_EXPIRES_IN_SECONDS", cast=int, default=60*60*24*30)
