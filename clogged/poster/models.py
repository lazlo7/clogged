from clogged.models import Base
from sqlalchemy import Integer, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column


class Poster(Base):
    __tablename__ = "posters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(16), unique=True)
    # A hashed and salted password using argon2. 
    credentials: Mapped[str] = mapped_column(TEXT)
