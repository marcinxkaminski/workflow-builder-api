from ml.components import __all__ as WORKFLOW_ELEMENTS

workflow_elements = {e.id: e for e in (Element[Element.CLASSNAME]() for Element in WORKFLOW_ELEMENTS)}


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


async def process_online(self, id: str, data: dict) -> dict:
    """
    Handles simple online processing of the data
    **workflow_element_name**: workflow element's name that should be used
    **data**: data to process
    **returns**: dict with result of the data processing
    """
    if (id in workflow_elements and
            hasattr('quick_main', workflow_elements[id])):
        return workflow_elements[id].quick_main(data=data)
