from secrets import token_urlsafe
from fastapi import Response
from redis.asyncio import Redis


async def generate_session_id() -> str:
    """Returns a url-safe 256 bit long random session id."""
    return token_urlsafe(32)


async def get_current_user(session_id: str, redis_client: Redis) -> int | None:
    """Returns the user id by the given session id or None if session id is invalid."""
    user_id = await redis_client.get(session_id)
    return int(user_id) if user_id else None


async def invalidate_session_cookie(response: Response):
    """Enriches given `response` with an empty immediately expiring session_id cookie."""
    response.set_cookie(
        "session_id", 
        "",
        max_age=0,
        secure=True, 
        httponly=True,
        samesite="strict"
    )
