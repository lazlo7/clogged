from clogged.redis import get_redis
from clogged.auth.utils import get_current_user
from typing import Annotated
from redis.asyncio import Redis
from fastapi import Cookie, Depends, HTTPException


async def verify_user_auth(
    session_id: Annotated[str | None, Cookie()] = None, 
    redis_client: Redis = Depends(get_redis)
) -> int:
    if session_id is None:
        raise HTTPException(status_code=401, detail="Session id is required")
    
    user_id = await get_current_user(session_id, redis_client)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid or expired session id")

    return user_id
