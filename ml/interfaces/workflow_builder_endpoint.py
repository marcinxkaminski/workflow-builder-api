from ml.utils.logger import get_logger
from aiohttp.web import Request, Response
from ml.interfaces.endpoint import RestEndpoint
from ml.core.workflow_builder import get_available_workflow_elements, build_workflow

logger = get_logger(__name__)


class WorkflowBuilderEndpoint(RestEndpoint):
    def __init__(self, *args, **kwargs):
        logger.info('Creating workflow builder endpoint ...')
        super().__init__(*args, **kwargs)

    async def get(self) -> Response:
        logger.info('Getting available workflow elements ...')
        return Response(status=200, body=(await get_available_workflow_elements()))

    async def post(self, request: Request) -> Response:
        logger.info('Creating new workflow ...')
        selected_workflow_elements = await request.json()
        return Response(status=200, body=(await build_workflow(selected_workflow_elements)))
