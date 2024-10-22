from pydantic import BaseModel, StringConstraints, NonNegativeInt
from typing_extensions import Annotated


UsernameType = Annotated[
    str, 
    StringConstraints(strip_whitespace=True, min_length=3, max_length=16, pattern=r'^[a-zA-Z0-9\-_]+$')
]

PlaintextPasswordType = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=6, max_length=32, pattern=r'^[a-zA-Z0-9\-_@$!%*#?&]+$')
] 

PosterIdType = NonNegativeInt


class PosterRegistrationModel(BaseModel):
    username: UsernameType
    password: PlaintextPasswordType


class PosterRegistrationResponseModel(BaseModel):
    poster_id: PosterIdType


class PosterModel(BaseModel):
    id: PosterIdType
    username: UsernameType
