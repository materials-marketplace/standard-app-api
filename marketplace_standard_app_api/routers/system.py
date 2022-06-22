from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from ..models.system import GlobalSearchResponse

router = APIRouter()


@router.get(
    "/globalSearch",
    operation_id="globalSearch",
    tags=["System"],
    responses={
        401: {"description": "Not authenticated."},
        422: {"description": "Validation error."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
    response_model=GlobalSearchResponse,
)
async def global_search(
    query: str, limit: Optional[int] = 100, offset: Optional[int] = 0
) -> GlobalSearchResponse:
    """Respond to global search queries."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "/health",
    operation_id="heartbeat",
    tags=["System"],
    response_class=HTMLResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        503: {"description": "Service unavailable."},
    },
)
async def heartbeat() -> HTMLResponse:
    """Check whether the application is running and available."""
    return HTMLResponse(content="<html><body>OK</body></html>", status_code=200)
