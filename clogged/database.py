from clogged.config import DATABASE_ASYNCPG_DSN
from clogged.blog.models import Base as BaseModel
from sqlalchemy.ext.asyncio import create_async_engine


async_engine = create_async_engine(
    DATABASE_ASYNCPG_DSN, 
    echo=True
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
