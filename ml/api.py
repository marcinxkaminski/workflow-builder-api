from ml.config import CLEANER, API
from ml.utils.logger import get_logger
from aiohttp.web import Application, run_app
from ml.interfaces.workflow_builder_interface import WorkflowBuilderInterface
from ml.utils.files import del_old_files_in_dir_periodic as run_cleaner

logger = get_logger(__name__)

app = Application()

workflow_builder_api = WorkflowBuilderInterface(API.get('ENDPOINTS', {}).get('WORKFLOW_BUILDER', '/'))
workflow_builder_api.register(router=app.router)

logger.info('Starting cleaner ...')
run_cleaner(interval=CLEANER.get('INTERVAL'), path=CLEANER.get('PATH'), age=CLEANER.get('AGE'))

logger.info('Starting api ...')
run_app(app, access_log=logger)
