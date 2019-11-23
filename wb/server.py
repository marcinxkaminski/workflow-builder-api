from uvicorn import run as run_app
from utils.cleaner import del_old_files_in_dir_periodic as run_cleaner
from utils.logger import get_logger
from config import CLEANER, API
from api import router as api
from cdn import router as cdn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

logger = get_logger(__name__)
app = FastAPI(title=API.get("TITLE"), description=API.get("DESCRIPTION"))

app.include_router(
    router=api,
    prefix=API.get("BASE_PATH", "{}").format(API.get("ENDPOINTS", {}).get("ELEMENTS")),
)
app.include_router(
    router=cdn,
    prefix=API.get("BASE_PATH", "{}").format(API.get("ENDPOINTS", {}).get("CDN")),
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=API.get("ORIGINS", ["*"]),
    allow_methods=API.get("METHODS", ["*"]),
    allow_headers=API.get("HEADERS", ["*"]),
    allow_credentials=API.get("ALLOW_CREDENTIALS", False),
)

if __name__ == "__main__":
    run_app(app, host=API.get("HOST"), port=API.get("PORT"))
    run_cleaner(
        interval=CLEANER.get("INTERVAL"),
        path=CLEANER.get("PATH"),
        age=CLEANER.get("AGE"),
    )
