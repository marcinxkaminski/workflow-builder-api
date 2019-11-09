from ml.components import __all__ as WORKFLOW_ELEMENTS

workflow_elements = {Element.NAME: Element() for Element in WORKFLOW_ELEMENTS}


async def get_available_workflow_elements(self) -> dict:
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
    } for e in workflow_elements.values() if e.optional]


async def process_online(self, name: str, data: dict) -> dict:
    """
    Handles simple online processing of the data
    **workflow_element_name**: workflow element's name that should be used
    **data**: data to process
    **returns**: dict with result of the data processing
    """
    if (name in workflow_elements and
            hasattr('quick_main', workflow_elements[name])):
        return workflow_elements[name].quick_main(data=data)
