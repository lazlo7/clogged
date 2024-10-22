from typing import Any
from fastapi import HTTPException
from clogged.blog.models import Poster
from argon2 import PasswordHasher
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


password_hasher = PasswordHasher()


async def get_posters(db: AsyncSession) -> list[dict[str, Any]]:
    """Returns a list of posters in the format of: {'id': poster_id, 'username': username}."""
    query = select(Poster.id, Poster.username)
    result = await db.execute(query)
    posters = [{"id": poster_id, "username": username} for poster_id, username in result.all()]
    return posters


async def add_poster(username: str, password: str, db: AsyncSession) -> int:
    """Ads a new poster with given username and password to the database and returns their's id."""
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
    return poster.id
