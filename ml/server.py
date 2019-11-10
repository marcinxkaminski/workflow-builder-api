from utils.files import del_old_files_in_dir_periodic as run_cleaner
from utils.logger import get_logger
from config import CLEANER, API
from api import router as api
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

pip from uvicorn import run as run_app

logger = get_logger(__name__)


if __name__ == "__main__":
    app = FastAPI(title=API.get('TITLE'), description=API.get('DESCRIPTION'))
    app.include_router(
        router=api,
        prefix=API.get('BASE_PATH', '{}').format(API.get('ENDPOINTS', {}).get('ELEMENTS'))
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=API.get('ORIGINS'),
        allow_methods=API.get('METHODS')
    )

    logger.info('Running app on %s:%s', API.get('HOST'), API.get('PORT'))
    run_app(app, host=API.get('HOST'), port=API.get('PORT'))
    run_cleaner(interval=CLEANER.get('INTERVAL'), path=CLEANER.get('PATH'), age=CLEANER.get('AGE'))
