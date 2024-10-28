from clogged.dependencies import get_db
from clogged.schemas import IdType
from clogged.poster.service import get_poster, get_posters
from clogged.poster.schemas import PosterModel
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/poster"
)


@router.get(
    "/posters",
    description="Returns all registered posters",
    response_model=list[PosterModel],
    status_code=200
)
async def get_all_posters(db: AsyncSession = Depends(get_db)):
    posters = await get_posters(db)
    return posters


@router.get(
    "/{poster_id}",
    description="Returns poster information by the given poster id",
    response_model=PosterModel,
    status_code=200
)
async def get_poster_info(
    poster_id: IdType,
    db: AsyncSession = Depends(get_db)
):
    poster = await get_poster(poster_id, db)
    if poster is None:
        raise HTTPException(status_code=404, detail="Poster with such id does not exist")
    return poster
