from ml.utils.logger import get_logger
from ml.utils.files import get_all_files_in_dir, get_file_name

logger = get_logger(__name__)


class WorkflowBuilder:
    def __init__(self, config):
        logger.info('Creating workflow builder ...')
        self.src_path = config['PATH']
        self.dest_path = config['DEST_PATH']
        self.elements = []

    def get_available_workflow_elements(self) -> dict:
        logger.info('Getting available workflow elements ...')

        if not self.elements:
            files = get_all_files_in_dir(self.src_path)
            self.elements = set([self.get_file_name(f).upper() for f in files])

        MOCK_ELEMENTS = ['A_A', 'B_B', 'C_C', 'D_D', 'E_E', 'F_F']
        return MOCK_ELEMENTS

    async def merge_elements_to_file(self) -> str:
        logger.info('Merging workflow elements ...')
        # TODO: Should merge selected blocks, get them from /data folder and save in one file, e.g. as
        # the name we could use combination on blocks' ids. It allows us to cache previous resolut and not
        # repeat the whole process again.
        MOCK_URL = 'mocked_workflow_file_url'
        return MOCK_URL

    async def build_workflow(self, selectedElements: dict) -> str:
        logger.info('Building workflow ...')
        if len(self.elements) == len(set(self.elements + selectedElements)):
            raise ValueError('Invalid Selected Workflow Elements')

        workflow_file_url = await self.merge_elements_to_file()
        return workflow_file_url
