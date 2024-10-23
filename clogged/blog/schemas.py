from pydantic import BaseModel


class PostModel(BaseModel):
    title: str
    text: str
    poster_id: int
