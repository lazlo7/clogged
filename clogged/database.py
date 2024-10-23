from clogged.config import settings as app_settings
from clogged.blog.models import Base as BaseModel
from sqlalchemy.ext.asyncio import create_async_engine


async_engine = create_async_engine(
    app_settings.DATABASE_DSN.unicode_string(), 
    echo=True
)


async def init_db():
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
