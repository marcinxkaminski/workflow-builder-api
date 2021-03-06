from fastapi import APIRouter
from pydantic import BaseModel
import wb.workflow_builder as wb
import wb.workflow_elements as we


class WorkflowElements(BaseModel):
    elements: list = []


class OnlineProcessingRequest(BaseModel):
    id: str = "element_id"
    data: dict = {"data": "any data to process"}


class BuildWorkflowResponse(BaseModel):
    id: str = "workflow_id"


router = APIRouter()


@router.get(
    path="/",
    response_description="List of workflow elements available to select.",
    response_model=WorkflowElements,
    status_code=200,
)
async def get_available_workflow_elements() -> WorkflowElements:
    """
    Get available workflow elements which you could use to build a workflow:
    **returns**: array with workflow's elements names
    """
    return {"elements": await we.get_available_workflow_elements()}


@router.put(
    path="/",
    response_description="Result of the online processing of the data.",
    status_code=200,
)
async def process_online(req: OnlineProcessingRequest):
    """
    Processes the data online
    **returns**: dict with online process result
    """
    return await we.process_online(id=req.id, data=req.data)


@router.post(
    path="/",
    response_description="URL to the workflow created from selected elements.",
    response_model=BuildWorkflowResponse,
    status_code=200,
)
async def build_workflow(req: WorkflowElements) -> BuildWorkflowResponse:
    """
    Creates workflow from selected workflow elements.
    **selected_workflow_elements**: array of selected workflow elements' names
    **returns**: url to complete workflow file
    """
    id = await wb.build_workflow(selected_elements=req.elements)
    return {"id": id}
