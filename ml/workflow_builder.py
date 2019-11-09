from config import BUILDER, API
from uuid import uuid4
from zipfile import ZipFile
from workflow_elements import workflow_elements


async def _zip_files(filepath: str, files: list) -> ZipFile:
    zip = ZipFile(filepath, 'w')
    for file in files:
        zip.write(file)
    zip.close()
    return zip


async def _merge_elements_to_file(wf_elems: list) -> str:
    files = []
    filepath = '{}/{}.zip'.format(BUILDER.DEST_PATH, uuid4())
    await _zip_files(filepath=filepath, files=files)
    return filepath
    pass


async def build_workflow(selected_elements: list) -> ZipFile:
    """
    Builds a workflow (file) from selected elements
    **selected_elements**: list of selected workflow elements' names
    :returns: url to complete workflow file
    """
    if not selected_elements:
        raise ValueError('No workflow elements selected')

    filepath = await _merge_elements_to_file(wf_elems=selected_elements)
    return '{}{}/{}'.format(API['BASE_PATH'], API['ENDPOINTS'].get('FILES', '/'), filepath)
