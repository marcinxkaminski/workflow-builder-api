from ml.utils.logger import get_logger
from aiohttp.web_urldispatcher import UrlDispatcher
from ml.interfaces.workflow_builder_endpoint import WorkflowBuilderEndpoint

logger = get_logger(__name__)


class WorkflowBuilderInterface:
    def __init__(self, endpoint_path: str):
        logger.info('Creating workflow builder interface ...')
        self.endpoint = endpoint_path
        self.workflow_builder_endpoint = WorkflowBuilderEndpoint()

    def register(self, router: UrlDispatcher):
        logger.info('Regisetring workflow builder interface ...')
        router.add_route('*', self.endpoint, self.workflow_builder_endpoint.dispatch)
