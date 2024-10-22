from clogged.dependencies import get_db
from clogged.admin.dependencies import verify_admin_key
from clogged.admin.schemas import PosterModel, PosterRegistrationModel, PosterRegistrationResponseModel
from clogged.admin.service import add_poster, get_poster, get_posters, remove_poster, update_poster_info
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/admin", 
    dependencies=[
        Depends(verify_admin_key)
    ]
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
    "/poster/{poster_id}",
    description="Returns poster information by the given poster id",
    response_model=PosterModel,
    status_code=200
)
async def get_poster_info(
    poster_id: int,
    db: AsyncSession = Depends(get_db)
):
    poster = await get_poster(poster_id, db)
    return poster 


@router.post(
    "/poster", 
    description="Registers a new poster with a given username and password and returns the poster's id",
    response_model=PosterRegistrationResponseModel,
    status_code=201
)
async def create_poster(
    registration_data: PosterRegistrationModel,
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
    poster_id: int,
    db: AsyncSession = Depends(get_db)
):
    poster = await remove_poster(poster_id, db)
    return poster


@router.put(
    "/poster/{poster_id}",
    description="Updates poster information by the given poster id",
    response_model=PosterModel,
    status_code=200
)
async def update_poster(
    poster_id: int,
    new_poster_data: PosterRegistrationModel,
    db: AsyncSession = Depends(get_db)
):
    poster = await update_poster_info(poster_id, new_poster_data.username, new_poster_data.password, db)
    return poster
