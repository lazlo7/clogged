import uvicorn
from clogged.config import settings as app_settings


def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("clogged.main:app", host="0.0.0.0", port=app_settings.CLOGGED_API_PORT, reload=app_settings.CLOGGED_IS_DEVELOPMENT)
