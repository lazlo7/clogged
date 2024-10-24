from clogged.database import init_db
from clogged.admin.routes import router as admin_router
from clogged.auth.routes import router as auth_router
from clogged.poster.routes import router as poster_router 
from contextlib import asynccontextmanager
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(_: FastAPI):        
    await init_db()
    yield


app = FastAPI(
    title="Clogged API",
    description="API for \"clogged\" - a simple blogging service.",
    version="1.0.0",
    root_path="/api/v1",
    lifespan=lifespan
)


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(poster_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
