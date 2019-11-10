from fastapi import APIRouter
from config import CDN
from starlette.responses import FileResponse


router = APIRouter()


@router.get(
    path='/',
    response_description='Returns the workflow file',
    status_code=200)
async def get_workflow_file(id: str = '') -> FileResponse:
    return FileResponse(path='{}/{}.zip'.format(CDN.get('PATH', '.'), id))
