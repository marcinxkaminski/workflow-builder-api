from fastapi import APIRouter
from config import CDN
from starlette.responses import FileResponse
from os import path

router = APIRouter()


@router.get(path="/", response_description="Returns the workflow file", status_code=200)
async def get_workflow_file(id: str = "") -> FileResponse:
    filepath = path.join(CDN.get("PATH", "."), f"{id}.zip")
    return FileResponse(
        path=filepath, filename=CDN.get("WORKFLOW_FILENAME", "workflow")
    )
