from clogged.config import REDIS_DSN
from redis.asyncio import Redis


async def get_redis() -> Redis:
    # TODO: Consider adding pooled connection and maybe reuse the same connection (?)
    # like with sqlalchemy's async sesion maker.
    return await Redis.from_url(
        REDIS_DSN,
        encoding="utf-8",
        decode_responses=True
    )
