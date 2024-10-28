from clogged.dependencies import get_db
from clogged.schemas import IdType
from clogged.post.dependencies import sanitize_post_input_data, verify_poster_authorship
from clogged.post import service as post_service
from clogged.post.schemas import (
    PostCreationModel, 
    PostInfoModel, 
    PostModel, 
    PostOffset, 
    PostLimit,
    TagModel
) 
from clogged.auth.dependencies import verify_user_auth
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/post",
    tags=["post"]
)


@router.get(
    "/{post_id}",
    description="Returns post by the given post id",
    response_model=PostModel,
    status_code=200
)
async def get_post(
    post_id: IdType,
    db: AsyncSession = Depends(get_db)
):
    post = await post_service.get_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=404, detail="Post with such id does not exist")
    return post
    

# TODO: Add an ability to provide a poster username to filter by,
# so that the poster would be able to modify/delete their posts, knowing post ids. 
@router.get(
    "/latest/",
    description="Returns the latest posts info by the given offset, \
                limit and containing at least one of the given tags",
    response_model=list[PostInfoModel],
    status_code=200
)
async def get_posts(
    tags: list[str] | None = Query(None, alias="tag"),
    offset: PostOffset = 0,
    limit: PostLimit = 5,
    db: AsyncSession = Depends(get_db)
):
    posts = await post_service.get_latest_posts_info(tags, limit=limit, offset=offset, db=db)
    return posts


@router.post(
    "/",
    description="Creates a new post and returns the post's id",
    response_model=PostInfoModel,
    status_code=201
)
async def create_post(
    post_data: PostCreationModel = Depends(sanitize_post_input_data),
    poster_id: int = Depends(verify_user_auth),
    db: AsyncSession = Depends(get_db)
):
    post_info = await post_service.add_post(
        tags=post_data.tags, 
        poster_id=poster_id, 
        title=post_data.title, 
        text=post_data.text, 
        db=db
    )

    return post_info


@router.put(
    "/{post_id}",
    description="Updates post by the given post id",
    response_model=PostModel,
    status_code=200
)
async def update_post(
    post_data: PostCreationModel = Depends(sanitize_post_input_data),
    verified_post_id: int = Depends(verify_poster_authorship),
    db: AsyncSession = Depends(get_db)
):
    post = await post_service.modify_post(
        new_tags=post_data.tags,
        post_id=verified_post_id,
        new_title=post_data.title,
        new_text=post_data.text,
        db=db
    )
    if post is None:
        # Should not happen, since verify_poster_authorship dependency ensures that the post exists,
        # but we'll check the return value of modify_post just in case.
        raise HTTPException(status_code=404, detail="Post with such id does not exist")

    return post


@router.delete(
    "/{post_id}",
    description="Deletes post by the given post id",
    response_model=PostInfoModel,
    status_code=200
)
async def delete_post(
    db: AsyncSession = Depends(get_db),
    post_id: int = Depends(verify_poster_authorship)
):
    post = await post_service.remove_post(post_id, db)
    if post is None:
        # Should not happen, since verify_poster_authorship dependency ensures that the post exists,
        # but we'll check the return value of remove_post just in case.
        raise HTTPException(status_code=404, detail="Post with such id does not exist")

    return post


@router.get(
    "/tags/",
    description="Returns all tags",
    tags=["tag"],
    response_model=list[TagModel],
    status_code=200
)
async def get_tags(
    db: AsyncSession = Depends(get_db)
):
    tags = await post_service.get_all_tags(db)
    return tags


@router.post(
    "/tag/{tag}",
    description="Creates a new tag",
    tags=["tag"],
    response_model=TagModel,
    dependencies=[
        Depends(verify_user_auth)
    ],
    status_code=201
)
async def create_tag(
    tag: str,
    db: AsyncSession = Depends(get_db)
):
    added_tag = await post_service.add_tag(tag, db)
    if added_tag is None:
        raise HTTPException(status_code=409, detail="Tag with such name already exists")
    return added_tag


@router.delete(
    "/tag/{tag}",
    description="Deletes a tag",
    tags=["tag"],
    response_model=TagModel,
    dependencies=[
        Depends(verify_user_auth)
    ],
    status_code=200
)
async def delete_tag(
    tag: str,
    db: AsyncSession = Depends(get_db)
):
    deleted_tag = await post_service.delete_tag(tag, db)
    if deleted_tag is None:
        raise HTTPException(status_code=404, detail="Tag with such name does not exist")
    return deleted_tag
