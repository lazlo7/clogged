from typing import Annotated
from clogged.auth.utils import invalidate_session_cookie
from clogged.redis import get_redis
from clogged.dependencies import get_db
from clogged.poster.schemas import PosterModel
from clogged.poster.service import get_poster
from clogged.auth.config import settings as auth_settings
from clogged.auth.service import (
    authenticate_user, 
    create_session, 
    invalidate_session, 
    invalidate_all_user_sessions
)
from clogged.auth.dependencies import verify_user_auth
from clogged.auth.schemas import PosterAuthModel, PosterLogoutResponseModel
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.get(
    "/check",
    description="Checks whether the user is authenticated by provided session_id and returns the user's info on success",
    response_model=PosterModel,
    status_code=200
)
async def is_authenticated(
    user_id: int = Depends(verify_user_auth),
    db: AsyncSession = Depends(get_db)
):
    # get_poster() is assumed to never return None since the user must exist at this point by verify_user_auth. 
    return await get_poster(user_id, db)


@router.post(
    "/login",
    description="Authenticates user by the given username and password and returns the user's id",
    response_model=PosterModel,
    status_code=200
)
async def login(
    login_data: PosterAuthModel,
    response: Response,
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_redis)
):
    poster = await authenticate_user(login_data.username, login_data.password, db)
    if poster is None:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    session_id = await create_session(poster["id"], cache)
    response.set_cookie(
        "session_id", 
        session_id,
        max_age=auth_settings.CLOGGED_SESSION_EXPIRES_IN_SECONDS,
        secure=True, 
        httponly=True,
        # Set a strict same-site cookie policy to prevent basic CSRF attacks.
        # TODO: Introduce CSRF tokens to completely eliminate CSRF attacks.
        #   The current method still allows for CSRF to be perfomed within the same site,
        #   even though we properly sanitize all user-controlled data to prevent XSS to be used for CSRF.
        samesite="strict"
    )
    return poster


@router.post(
    "/logout",
    description="Logs out the user by the given user id and returns the logged out user and the number of removed sessions",
    response_model=PosterLogoutResponseModel,
    status_code=200
)
async def logout(
    response: Response,
    everywhere: bool = False,
    user_id: int = Depends(verify_user_auth),
    session_id: Annotated[str | None, Cookie()] = None,
    db: AsyncSession = Depends(get_db),
    cache: Redis = Depends(get_redis)
):
    if session_id is None:
        # Should not ever happen since session_id is guaranteed to be valid by the verify_user_auth dependency.
        raise HTTPException(status_code=401, detail="Session id is required")
    
    sessions_revoked_n = await invalidate_all_user_sessions(user_id, cache) if everywhere \
                         else int(await invalidate_session(session_id, cache))
    
    await invalidate_session_cookie(response)

    poster = await get_poster(user_id, db)
    if poster is None:
        # Should not ever happen since poster is guaranteed to exist by the verify_user_auth dependency.
        raise HTTPException(status_code=500, detail="Could not find the user by the given user id")

    poster["sessions_revoked_n"] = sessions_revoked_n
    return poster
