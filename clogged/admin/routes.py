from clogged.dependencies import get_db
from clogged.redis import get_redis
from clogged.schemas import IdType
from clogged.admin.dependencies import verify_admin_key
from clogged.admin.service import add_poster, remove_poster, update_poster_info
from clogged.auth.schemas import PosterAuthModel
from clogged.poster.schemas import PosterModel
from redis.asyncio import Redis
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


"""Private admin-only poster API: create, read, update and delete full poster info."""
router = APIRouter(
    prefix="/admin", 
    dependencies=[
        Depends(verify_admin_key)
    ]
)

# TODO: Add full poster info (id, username and credentials) get endpoint.

@router.post(
    "/poster", 
    description="Registers a new poster with a given username and password and returns the poster's id",
    response_model=PosterModel,
    status_code=201
)
async def create_poster(
    registration_data: PosterAuthModel,
    db: AsyncSession = Depends(get_db)
):
    poster_id = await add_poster(registration_data.username, registration_data.password, db)
    return poster_id    


@router.delete(
    "/poster/{poster_id}",
    description="Unregisters a poster by the given poster id and returns the removed poster", 
    response_model=PosterModel,
    status_code=200
)
async def delete_poster(
    poster_id: IdType,
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_redis)
):
    poster = await remove_poster(poster_id, db, cache)
    return poster


@router.put(
    "/poster/{poster_id}",
    description="Updates poster information by the given poster id",
    response_model=PosterModel,
    status_code=200
)
async def update_poster(
    poster_id: IdType,
    new_poster_data: PosterAuthModel,
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_redis)
):
    poster = await update_poster_info(poster_id, new_poster_data.username, new_poster_data.password, db, cache)
    return poster
