from typing import Any
from clogged.poster.models import Poster
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


async def get_posters(db: AsyncSession) -> list[dict[str, Any]]:
    """Returns a list of posters in the format of: {'id': poster_id, 'username': username}."""
    query = select(Poster.id, Poster.username)
    result = await db.execute(query)
    posters = [{"id": poster_id, "username": username} for poster_id, username in result.all()]
    return posters


async def get_poster(poster_id: int, db: AsyncSession) -> dict[str, Any] | None:
    """
    Returns poster in the format of: {'id': poster_id, 'username': username} 
    by the given id or None if poster does not exist.
    """
    query = select(Poster.id, Poster.username).where(Poster.id == poster_id)
    result = (await db.execute(query)).first()
    if result is None:
        return None
    
    return {"id": result.id, "username": result.username}
