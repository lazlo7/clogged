from clogged.dependencies import get_db
from clogged.post.service import get_post
from clogged.auth.dependencies import verify_user_auth
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


async def verify_poster_authorship(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    poster_id: int = Depends(verify_user_auth),
) -> int:
    """
    Checks that the given `poster_id` is the author of the post with the given `post_id`.
    Returns the `post_id` if the authorship is verified, otherwise raises a relevant HTTPException.
    """
    post = await get_post(post_id, db)
    if post is None:
        raise HTTPException(status_code=404, detail="Post with such id does not exist")
    
    if post["poster_id"] != poster_id:
        raise HTTPException(status_code=403, detail="You are not the author of the post")
    
    return post_id
