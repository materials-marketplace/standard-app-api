from typing import Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response

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


@router.get(
    "/info",
    operation_id="getInfo",
    summary="Returns system information.",
    responses={
        404: {"description": "Not found."},
        501: {"description": "Not implemented."},
    },
)
async def get_info() -> JSONResponse:
    """Return information related to the application.

    The application developer may decide what information, and define their own
    filter parameters (generally query parameters).
    """
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "/logs",
    operation_id="getLogs",
    summary="Returns logs from the application.",
    responses={
        404: {"description": "Not found."},
        501: {"description": "Not implemented."},
    },
)
async def get_logs(id: Optional[str], limit: int = 100, offset: int = 0) -> Response:
    """Return application logs.

    If an id is provided, the logs will be for a specific entity (transformation, collection or dataset).
    """
    raise HTTPException(status_code=501, detail="Not implemented.")
