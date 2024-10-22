from clogged.database import init_db
from clogged.config import DATABASE_DSN
from clogged.admin.routes import router as admin_router
from contextlib import asynccontextmanager
from asyncpg import create_pool
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.postgres_pool = await create_pool(
            dsn=DATABASE_DSN,
            min_size=4,
            max_size=16
        )
        await init_db()
        yield
    finally:
        await app.state.postgres_pool.close()


app = FastAPI(
    title = "Clogged API",
    description = "API for \"clogged\" - a simple blogging service.",
    version = "1.0.0",
    lifespan=lifespan
)


app.include_router(admin_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
