from clogged.config import ADMIN_API_KEY
from fastapi import HTTPException, Header
from typing_extensions import Annotated


async def verify_admin_key(X_Api_Key: Annotated[str, Header()]):
    if X_Api_Key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid X-Api-Key header")
