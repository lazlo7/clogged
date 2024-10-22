from clogged.dependencies import get_db
from clogged.admin.dependencies import verify_admin_key
from clogged.admin.schemas import PosterModel, PosterRegistrationModel, PosterRegistrationResponseModel
from clogged.admin.service import add_poster, get_posters
from fastapi import APIRouter, Request, Depends
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
    status_code = 200
)
async def get_all_posters(db: AsyncSession = Depends(get_db)):
    posters = await get_posters(db)
    return posters


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
    return PosterRegistrationResponseModel(poster_id=poster_id)    


@router.delete("/poster", status_code=201)
async def delete_poster(r: Request):
    pass
