from clogged.blog.schemas import PostModel 
from fastapi import APIRouter


router = APIRouter(
    prefix="/post", 
)

@router.post(
    "/",
    description="Creates a new post and returns the post's id",
    response_model=PostModel,
    status_code=201
)
async def create_post(
    post_data: PostModel
):
    pass
    