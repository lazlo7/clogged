from sqlalchemy import Integer, VARCHAR, TEXT, ForeignKey, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Poster(Base):
    __tablename__ = "posters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(16), unique=True)
    # A hashed and salted password using argon2. 
    credentials: Mapped[str] = mapped_column(TEXT)


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    poster_id: Mapped[int] = mapped_column(ForeignKey("posters.id"))
    title: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[int] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    # TODO: look into document-oriented databases, which may be better at storing large texts
    # and providing search functions on them.
    text: Mapped[str] = mapped_column(TEXT)


class PostTag(Base):
    __tablename__ = "post_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, unique=True)
    name: Mapped[str] = mapped_column(TEXT, unique=True)


class TaggedPosts(Base):
    __tablename__ = "tagged_posts"
    
    # The primary key is a composite of post_id and tag_id.
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("post_tags.id"), primary_key=True)
