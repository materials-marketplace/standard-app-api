from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["FrontPage"],
    responses={
        404: {"description": "Not found."},
    },
)


@router.get(
    "/",
    operation_id="frontend",
    summary="Open the frontend of the app",
    response_class=HTMLResponse,
)
async def frontpage() -> HTMLResponse:
    """Open the frontpage of the app."""
    raise HTTPException(status_code=501, detail="Not implemented.")
