from typing import Annotated
from datetime import datetime
from annotated_types import Le, Lt
from pydantic import BaseModel, NonNegativeInt


PostOffset = NonNegativeInt
PostLimit = Annotated[NonNegativeInt, Le(100)]


class PostModel(BaseModel):
    id: NonNegativeInt
    poster_id: NonNegativeInt
    title: str
    created_at: datetime
    tags: list[str]
    text: str


class PostInfoModel(BaseModel):
    id: NonNegativeInt
    poster_id: NonNegativeInt
    title: str
    created_at: datetime
    tags: list[str]


class PostCreationModel(BaseModel):
    title: str
    tags: list[str]
    text: str


class TagModel(BaseModel):
    tag: str
