from typing import Any
from fastapi import HTTPException
from clogged.blog.models import Poster
from argon2 import PasswordHasher
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession


password_hasher = PasswordHasher()


async def get_posters(db: AsyncSession) -> list[dict[str, Any]]:
    """Returns a list of posters in the format of: {'id': poster_id, 'username': username}."""
    query = select(Poster.id, Poster.username)
    result = await db.execute(query)
    posters = [{"id": poster_id, "username": username} for poster_id, username in result.all()]
    return posters


async def get_poster(poster_id: int, db: AsyncSession) -> dict[str, Any]:
    """
    Returns poster in the format of: {'id': poster_id, 'username': username} by the given id.
    Throws an HTTPException with a relevent detail if poster with such id does not exist.
    """
    query = select(Poster.id, Poster.username).where(Poster.id == poster_id)
    result = (await db.execute(query)).first()
    if result is None:
        raise HTTPException(status_code=404, detail="Poster with such id does not exist")
    
    return {"id": result.id, "username": result.username}


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
    return {"poster_id": poster.id}


async def remove_poster(poster_id: int, db: AsyncSession) -> dict[str, Any]:
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
    return removed_poster


async def update_poster_info(
    poster_id: int, 
    new_username: str, 
    new_password: str, 
    db: AsyncSession
) -> dict[str, Any]:
    """Updates poster information by the given poster id and returns the updated poster."""
    query = select(Poster).filter(Poster.id == poster_id)
    poster = (await db.execute(query)).scalar()
    if poster is None:
        raise HTTPException(status_code=404, detail="Poster with such id does not exist")

    poster.username = new_username
    poster.credentials = password_hasher.hash(new_password)

    await db.commit()
    return {
        "id": poster.id,
        "username": poster.username
    }
