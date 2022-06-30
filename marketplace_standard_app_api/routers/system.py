from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from ..models.system import GlobalSearchResponse

router = APIRouter(
    tags=["System"],
)


@router.get(
    "/globalSearch",
    operation_id="globalSearch",
    summary="Respond to global search queries",
    responses={
        422: {"description": "Validation error."},
        501: {"description": "Not implemented."},
    },
    response_model=GlobalSearchResponse,
)
async def global_search(
    q: str, limit: Optional[int] = 100, offset: Optional[int] = 0
) -> GlobalSearchResponse:
    """Respond to global search queries."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "/health",
    operation_id="heartbeat",
    summary="Check if the application is running and available",
    response_class=HTMLResponse,
)
async def heartbeat() -> HTMLResponse:
    """Check whether the application is running and available."""
    return HTMLResponse(content="<html><body>OK</body></html>", status_code=200)
