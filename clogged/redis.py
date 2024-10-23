from clogged.config import settings as app_settings
from redis.asyncio import Redis


async def get_redis() -> Redis:
    # TODO: Consider adding pooled connection and maybe reuse the same connection (?)
    # like with sqlalchemy's async sesion maker.
    return await Redis.from_url(
        app_settings.REDIS_DSN.unicode_string(),
        encoding="utf-8",
        decode_responses=True
    )
