from fastapi import APIRouter
from pydantic import BaseModel
from config import BUILDER
from workflow_builder import WorkflowBuilder


class WorkflowElements(BaseModel):
    elements: list = []


router = APIRouter()
wfb = WorkflowBuilder(BUILDER)


@router.get(
    path='/',
    response_description='List of workflow elements available to select.',
    response_model=WorkflowElements,
    status_code=200
)
async def get_available_workflow_elements():
    """
    Get available workflow elements which you could use to build a workflow:
    **returns**: array with workflow's elements names
    """
    return wfb.get_available_workflow_elements()


@router.post('/')
async def build_workflow(selected_workflow_elements: WorkflowElements):
    """
    Creates workflow from selected workflow elements.
    **selected_workflow_elements**: array of selected workflow elements' names
    **returns**: url to complete workflow file
    """
    return await wfb.build_workflow(selected_workflow_elements.elements)
