from typing import Any
from clogged.config import SESSION_EXPIRES_IN_SECONDS
from clogged.auth.utils import generate_session_id
from clogged.poster.models import Poster
from argon2 import PasswordHasher
from argon2.exceptions import VerificationError, InvalidHashError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis


password_hasher = PasswordHasher()


async def invalidate_session(session_id: str, redis_client: Redis) -> bool:
    """Invalidates the session by the given session id and returns whether it succeeded."""
    return bool(await redis_client.delete(session_id))
    

async def invalidate_all_user_sessions(user_id: int, redis_client: Redis) -> int:
    """Invalidates all sessions by the given user id and returns the number of invalidated sessions."""
    sessions_invalidated_n = 0
    keys = await redis_client.keys("*")
    for key in keys:
        if await redis_client.get(key) == str(user_id):
            sessions_invalidated_n += await invalidate_session(key, redis_client)
    
    return sessions_invalidated_n


async def create_session(user_id: int, redis_client: Redis) -> str:
    """Creates a new session for the given user id and returns the session id."""
    session_id = await generate_session_id()
    await redis_client.set(session_id, user_id, ex=SESSION_EXPIRES_IN_SECONDS)
    return session_id


async def authenticate_user(username: str, password: str, db: AsyncSession) -> dict[str, Any] | None:
    """
    Attempts to authenticate user by the given username and password.

    Returns the user id and username in the format of {"id": user_id, "username": username} 
    if authentication succeeded, otherwise returns None.
    """
    query = select(Poster).where(Poster.username == username)
    poster = (await db.execute(query)).scalar()
    if poster is None:
        # Poster with such username does not exist.
        return None
    try:
        password_hasher.verify(poster.credentials, password)
    except (VerificationError, InvalidHashError):
        # Password hashes do not match.
        return None

    # Passed password verification -> need to check if the password needs to be rehashed.
    if password_hasher.check_needs_rehash(poster.credentials):
        poster.credentials = password_hasher.hash(password)
        await db.commit()

    return {"id": poster.id, "username": poster.username}
