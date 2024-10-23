from clogged.auth.schemas import UsernameType
from pydantic import BaseModel, NonNegativeInt


class PosterModel(BaseModel):
    id: NonNegativeInt
    username: UsernameType
