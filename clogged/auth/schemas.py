from typing import Annotated
from pydantic import StringConstraints, BaseModel, NonNegativeInt


UsernameType = Annotated[
    str, 
    StringConstraints(strip_whitespace=True, min_length=3, max_length=16, pattern=r'^[a-zA-Z0-9\-_]+$')
]

PlaintextPasswordType = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=6, max_length=32, pattern=r'^[a-zA-Z0-9\-_@$!%*#?&]+$')
]


class PosterAuthModel(BaseModel):
    username: UsernameType
    password: PlaintextPasswordType


class PosterLogoutResponseModel(BaseModel):
    id: NonNegativeInt
    username: UsernameType
    sessions_revoked_n: NonNegativeInt
