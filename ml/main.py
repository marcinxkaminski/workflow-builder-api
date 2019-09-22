from uvicorn import run as run_app
from fastapi import FastAPI
from api import router as api
from config import CLEANER, API
from utils.logger import get_logger
from utils.files import del_old_files_in_dir_periodic as run_cleaner

logger = get_logger(__name__)
app = FastAPI(title=API.get('TITLE'), description=API.get('DESCRIPTION'))

# logger.info('Starting cleaner ...')
# run_cleaner(interval=CLEANER.get('INTERVAL'), path=CLEANER.get('PATH'), age=CLEANER.get('AGE'))

logger.debug('Adding Workflow Builder API routes ...')
app.include_router(
    router=api,
    prefix=API.get('BASE_PATH', '{}').format(API.get('ENDPOINTS', {}).get('ELEMENTS'))
)

if __name__ == "__main__":
    logger.debug('Starting app ...')
    run_app(app, host="0.0.0.0", port=8000)
