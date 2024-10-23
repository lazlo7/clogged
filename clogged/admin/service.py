from typing import Any
from fastapi import HTTPException
from clogged.poster.models import Poster
from clogged.auth.service import invalidate_all_user_sessions, password_hasher
from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def add_poster(username: str, password: str, db: AsyncSession) -> dict[str, Any]:
    """Adds a new poster with the given username and password to the database and returns their's id."""
    # Check if such username already exists.
    query = select(Poster).where(Poster.username == username)
    result = await db.execute(query)
    if result.scalar() is not None:
        # Maybe not the best idea to couple http exceptions inside lower-level service
        # but it allows to make code much cleaner and readable.
        raise HTTPException(status_code=400, detail="Poster with such username already exists")
    
    credentials = password_hasher.hash(password)
    poster = Poster(username=username, credentials=credentials)
    
    db.add(poster)
    await db.commit()
    return {"id": poster.id, "username": poster.username}


async def remove_poster(poster_id: int, db: AsyncSession, cache: Redis) -> dict[str, Any]:
    """Removes poster by the given poster id from the database and returns back the removed poster."""
    query = select(Poster).filter(Poster.id == poster_id)
    poster = (await db.execute(query)).scalar()
    if poster is None:
        raise HTTPException(status_code=404, detail="Poster with such id does not exist")

    removed_poster = {
        "id": poster.id,
        "username": poster.username
    }

    await db.delete(poster)
    await db.commit()
    
    # Invalidate session in redis, so that the poster can't use an invalid id anymore.
    await invalidate_all_user_sessions(poster_id, cache)

    return removed_poster


async def update_poster_info(
    poster_id: int, 
    new_username: str, 
    new_password: str, 
    db: AsyncSession,
    cache: Redis
) -> dict[str, Any]:
    """Updates poster information by the given poster id and returns the updated poster."""
    query = select(Poster).filter(Poster.id == poster_id)
    poster = (await db.execute(query)).scalar()
    if poster is None:
        raise HTTPException(status_code=404, detail="Poster with such id does not exist")

    poster.username = new_username
    poster.credentials = password_hasher.hash(new_password)

    # Invalidate session in redis to force poster to relogin with new credentials.
    await invalidate_all_user_sessions(poster_id, cache)

    await db.commit()
    return {
        "id": poster.id,
        "username": poster.username
    }
