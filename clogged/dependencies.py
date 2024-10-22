from clogged.database import async_engine as async_database_engine
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import async_sessionmaker


AsyncSessionFactory = async_sessionmaker(
    bind=async_database_engine,
    autocommit=False, 
    autoflush=False, 
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator:
    async with AsyncSessionFactory() as session:
        yield session
