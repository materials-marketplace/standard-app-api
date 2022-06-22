from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

router = APIRouter(
    tags=["FrontPage"],
    responses={
        404: {"description": "Not found."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        503: {"description": "Service unavailable."},
    },
)


@router.get(
    "/",
    operation_id="frontend",
    response_class=HTMLResponse,
)
async def frontpage() -> HTMLResponse:
    """Open the frontpage of the app."""
    raise HTTPException(status_code=501, detail="Not implemented.")
