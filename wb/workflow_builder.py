from workflow_elements import WORKFLOW_ELEMENTS
from config import BUILDER
from zipfile import ZipFile
from uuid import uuid4
from aiofiles import open as aioopen
from os import mkdir, path, listdir
from shutil import copy2, rmtree


async def _create_workflow_directory(id: str) -> str:
    workflow_dir_path = path.join(BUILDER.get('DEST_PATH', '.'), id)

    if not path.exists(workflow_dir_path):
        mkdir(workflow_dir_path)

    return workflow_dir_path


async def _get_import_line(filename: str, classname: str):
    module = filename.split('.')[0]
    return f'from {module} import {classname}'


async def _get_main_function_call_line(classname: str, first: bool = False, independent: bool = True):
    input_file = 'input' if first or not independent else 'output'
    return f'    {classname}().main(input={input_file}, output=output, delimiter=delimiter, **kwargs)'


async def _get_workflow_components(elements: list) -> dict:
    imports = []
    calls = []
    requirements = []

    for e in WORKFLOW_ELEMENTS.values():
        if e.optional is False:
            files = [path.join(BUILDER.get('PATH', '.'), fn)
                     for fn in e.filenames]

    for idx, element in enumerate(elements):
        e = WORKFLOW_ELEMENTS.get(element.get('id'), {})
        if e and e.filenames and e.classname:
            requirements += e.requirements
            calls.append(
                await _get_main_function_call_line(
                    classname=e.classname,
                    first=(idx == 0),
                    independent=e.independent
                )
            )

            for i, e_filename in enumerate(e.filenames):
                filepath = '{}/{}'.format(BUILDER.get('PATH', '.'), e_filename)
                if filepath not in files:
                    files.append(filepath)

                if i == 0:
                    import_line = await _get_import_line(filename=e_filename, classname=e.classname)
                    if import_line not in imports:
                        imports.append(import_line)

    return {'files': files, 'imports': imports, 'calls': calls, 'requirements': set(requirements)}


async def _copy_files_to_dir(files: list, dir_path: str):
    for f in files:
        copy2(f, dir_path)


async def _create_main_file_in_workflow_dir(workflow_components: dict, dir_path: str):
    main_file_path = path.join(
        dir_path, BUILDER.get('MAIN_FILE_NAME', 'main.py'))

    async with aioopen(main_file_path, mode='w') as nf:
        async with aioopen(BUILDER.get('TEMPLATE_FILE'), mode='r') as f:
            async for line in f:
                if BUILDER.get('IMPORTS_COMMENT', 'IMPORT') in line:
                    await nf.write('\n'.join(workflow_components.get('imports', [])))
                elif BUILDER.get('MAIN_COMMENT', 'MAIN') in line:
                    await nf.write('\n'.join(workflow_components.get('calls', [])))
                else:
                    await nf.write(line)

    workflow_components['files'].append(main_file_path)


async def _create_requirements_file_in_workflow_dir(workflow_components: dict, dir_path: str):
    requirements_file_path = path.join(dir_path, BUILDER.get(
        'REQUIREMENTS_FILE_NAME', 'requirements.txt'))

    async with aioopen(requirements_file_path, mode='w') as requirements_file:
        await requirements_file.write('\n'.join(workflow_components.get('requirements', [])))

    workflow_components['files'].append(requirements_file_path)


async def _zip_workflow_dir(workflow_id: str, dir_path: str) -> str:
    zip_file_path = path.join(BUILDER.get(
        'DEST_PATH', '.'), f'{workflow_id}.zip')

    with ZipFile(zip_file_path, 'w') as zip:
        for filename in listdir(dir_path):
            filepath = path.join(dir_path, filename)
            zip.write(filepath)

    return zip_file_path


async def _delete_workflow_dir(dir_path: str) -> str:
    rmtree(dir_path, ignore_errors=True)


async def build_workflow(selected_elements: list) -> str:
    """
    Builds a workflow (file) from selected elements
    **selected_elements**: list of selected workflow elements' names
    :returns: created workflow id
    """
    if not selected_elements:
        raise ValueError('No workflow elements selected')

    workflow_id = str(uuid4())
    workflow_dir_path = await _create_workflow_directory(id=workflow_id)
    workflow_components = await _get_workflow_components(elements=selected_elements)

    await _copy_files_to_dir(files=workflow_components.get('files', []), dir_path=workflow_dir_path)
    await _create_main_file_in_workflow_dir(workflow_components=workflow_components, dir_path=workflow_dir_path)
    await _create_requirements_file_in_workflow_dir(workflow_components=workflow_components, dir_path=workflow_dir_path)
    await _zip_workflow_dir(workflow_id=workflow_id, dir_path=workflow_dir_path)
    await _delete_workflow_dir(dir_path=workflow_dir_path)

    return workflow_id
