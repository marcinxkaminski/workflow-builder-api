from wb.components import __all__ as WORKFLOW_ELEMENTS
from config import BUILDER, API
from zipfile import ZipFile
from uuid import uuid4
from aiofiles import open as aioopen

workflow_elements = {e.NAME: e for e in WORKFLOW_ELEMENTS}


async def _zip_files(filepath: str, files: list) -> str:
    zip_file_path = '{}.zip'.format(filepath)
    zip = ZipFile(zip_file_path, 'w')
    for file in files:
        zip.write(file)
    zip.close()
    return zip_file_path


async def _get_import(filename: str, classname: str):
    return 'from {} import {}'.format(filename.split('.')[0], classname)


async def _get_main_function_call(classname: str):
    return '{}().main(input=input, output=output, delimiter=delimiter, **kwargs)'


async def _get_file_components(wf_elems: list):
    files = []
    imports = []
    calls = []
    requirements = []

    for elem in wf_elems:
        e = workflow_elements.get(elem.name, {})
        if not e.FILE or not e.CLASSNAME:
            raise ValueError('Selected element is invalid')

        files.append(e.FILE)
        imports.append(_get_import(filename=e.FILE, classname=e.CLASSNAME))
        calls.append(_get_main_function_call(classname=e.CLASSNAME))
        requirements += e.REQUIREMENTS

    return {'files': files, 'imports': imports, 'calls': calls, 'requirements': set(requirements)}


async def _create_main_file(filepath: str, wf_elems: list):
    main_file_path = '{}.py'.format(filepath)
    requirements_file_path = '{}.txt'.format(filepath)
    workflow_file_components = _get_file_components(wf_elems=wf_elems)

    async with aioopen(main_file_path, mode='w') as nf:
        async with aioopen(BUILDER.get('TEMPLATE_FILE'), mode='r+') as f:
            async for line in f:
                if BUILDER.get('IMPORTS_COMMENT', 'IMPORT') in line:
                    nf.write('\n'.join(workflow_file_components.get('imports', [])))
                elif BUILDER.get('MAIN_COMMENT', 'MAIN') in line:
                    nf.write('\n'.join(workflow_file_components.get('calls', [])))
                else:
                    nf.write(line)

    async with aioopen(requirements_file_path, mode='w') as requirements_file:
        requirements_file.write('\n'.join(workflow_file_components.get('requirements', [])))

    files = workflow_file_components.get('files', [])
    files.append(main_file_path)
    files.append(requirements_file_path)

    return files


async def _merge_elements_to_file(wf_elems: list) -> str:
    uuid = uuid4()
    base_filepath = '{}/{}'.format(BUILDER.DEST_PATH, uuid)
    files = await _create_main_file(filepath=base_filepath, wf_elems=wf_elems)
    result_file_path = await _zip_files(filepath=base_filepath, files=files)
    return '{}/{}'.format(API.get('HOST', ''), result_file_path)


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
