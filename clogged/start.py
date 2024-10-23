import sys
import uvicorn
from clogged.config import settings as app_settings


def start():
    """Launched with `poetry run start` at root level"""
    is_development = "dev" in sys.argv
    uvicorn.run("clogged.main:app", host="0.0.0.0", port=app_settings.APP_API_PORT, reload=is_development)
