from clogged.config import settings as app_settings
from clogged.database import init_db
from clogged.admin.routes import router as admin_router
from clogged.auth.routes import router as auth_router
from clogged.post.routes import router as post_router
from clogged.poster.routes import router as poster_router 
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse


@asynccontextmanager
async def lifespan(_: FastAPI):        
    await init_db()
    yield


app = FastAPI(
    title="Clogged API",
    description="API for \"clogged\" - a simple blogging service.",
    version="1.0.0",
    root_path="/api/v1",
    # Always disable both Swagger and Redoc docs, favor Rapidoc.
    docs_url=None, 
    redoc_url=None,
    # Enable OpenAPI schema endpoint only if it's specified, 
    # since we may want to hide API docs in production.
    openapi_url="/openapi.json" if app_settings.CLOGGED_ENABLE_API_DOCS else None, 
    lifespan=lifespan
)


app.include_router(admin_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(poster_router)


# Explicitly define Rapidoc UI endpoint.
@app.get(
    "/docs",
    response_class=HTMLResponse,
    include_in_schema=False
)
async def get_rapidoc(r: Request):
    """Provide Rapidoc UI only if API docs are enabled."""
    if not app_settings.CLOGGED_ENABLE_API_DOCS:
        raise HTTPException(status_code=404, detail="API docs are disabled")
    
    return f"""
        <!doctype html>
        <html>
        <head>
            <meta charset="utf-8">
            <script type="module" src="https://unpkg.com/rapidoc/dist/rapidoc-min.js"></script>
        </head>
        <body>
            <rapi-doc
                spec-url="{r.app.openapi_url}"
                theme = "dark">
            </rapi-doc>
        </body>
        </html>
    """
