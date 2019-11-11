from components.WorkflowElement import WorkflowElement
from components.End import End
from components.Start import Start
from components.Normalize import Normalize

WORKFLOW_ELEMENTS = {e.id: e for e in (WorkflowElement(), End(), Start(), Normalize())}


async def get_available_workflow_elements() -> list:
    """
    Get availble worfklow's elements.
    :returns: list of avaible workflow elements' names
    """
    return [{
        'id': e.id,
        'name': e.name,
        'config': e.config,
        'description': e.description,
        'materialIcon': e.materialIcon
    } for e in WORKFLOW_ELEMENTS.values() if e.optional]


async def process_online(id: str, data: dict):
    """
    Handles simple online processing of the data
    **workflow_element_name**: workflow element's name that should be used
    **data**: data to process
    **returns**: dict with result of the data processing
    """
    if (id in WORKFLOW_ELEMENTS and
            hasattr(WORKFLOW_ELEMENTS[id], 'quick_main')):
        return WORKFLOW_ELEMENTS[id].quick_main(data=data)
