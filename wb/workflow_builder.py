from workflow_elements import WORKFLOW_ELEMENTS
from config import BUILDER
from zipfile import ZipFile
from uuid import uuid4
from aiofiles import open as aioopen


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
    return '    {}().main(input=input, output=output, delimiter=delimiter, **kwargs)'.format(classname)


async def _get_file_components(wf_elems: list):
    imports = []
    calls = []
    requirements = []
    files = ['{}/{}'.format(BUILDER.get('PATH', '.'), e.filename) for e in WORKFLOW_ELEMENTS.values() if not e.optional]

    for elem in wf_elems:
        e = WORKFLOW_ELEMENTS.get(elem.get('id'), {})
        if not e.filename or not e.classname:
            raise ValueError('Selected element is invalid')

        files.append('{}/{}'.format(BUILDER.get('PATH', '.'), e.filename))
        imports.append(await _get_import(filename=e.filename, classname=e.classname))
        calls.append(await _get_main_function_call(classname=e.classname))
        requirements += e.requirements

    return {'files': files, 'imports': imports, 'calls': calls, 'requirements': set(requirements)}


async def _create_main_file(filepath: str, wf_elems: list):
    main_file_path = '{}.py'.format(filepath)
    requirements_file_path = '{}.txt'.format(filepath)
    workflow_file_components = await _get_file_components(wf_elems=wf_elems)

    async with aioopen(main_file_path, mode='w') as nf:
        async with aioopen(BUILDER.get('TEMPLATE_FILE'), mode='r') as f:
            async for line in f:
                if BUILDER.get('IMPORTS_COMMENT', 'IMPORT') in line:
                    await nf.write('\n'.join(workflow_file_components.get('imports', [])))
                elif BUILDER.get('MAIN_COMMENT', 'MAIN') in line:
                    await nf.write('\n'.join(workflow_file_components.get('calls', [])))
                else:
                    await nf.write(line)

    async with aioopen(requirements_file_path, mode='w') as requirements_file:
        await requirements_file.write('\n'.join(workflow_file_components.get('requirements', [])))

    files = workflow_file_components.get('files', [])
    files.append(main_file_path)
    files.append(requirements_file_path)

    return files


async def _merge_elements_to_file(wf_elems: list) -> str:
    uuid = str(uuid4())
    base_filepath = '{}/{}'.format(BUILDER.get('DEST_PATH', '.'), uuid)
    files = await _create_main_file(filepath=base_filepath, wf_elems=wf_elems)
    await _zip_files(filepath=base_filepath, files=files)
    return uuid


async def build_workflow(selected_elements: list) -> str:
    """
    Builds a workflow (file) from selected elements
    **selected_elements**: list of selected workflow elements' names
    :returns: url to complete workflow file
    """
    if not selected_elements:
        raise ValueError('No workflow elements selected')

    return await _merge_elements_to_file(wf_elems=selected_elements)
