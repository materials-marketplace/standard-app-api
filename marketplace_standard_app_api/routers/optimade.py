from http.client import HTTPException

from fastapi import APIRouter, Depends, Request
from optimade.models import StructureResponseMany, StructureResponseOne
from optimade.server.query_params import EntryListingQueryParams, SingleEntryQueryParams
from optimade.server.routers.versions import CsvResponse
from optimade.server.schemas import ERROR_RESPONSES

router = APIRouter(
    prefix="/optimade",
    tags=["Optimade"],
    responses={
        501: {"description": "Not implemented"},
    },
)


@router.get(
    "/versions",
    operation_id="getOptimadeVersions",
    response_class=CsvResponse,
    summary="Get the versions of optimade.",
    responses={
        404: {"description": "Not found"},
    },
)
def get_versions(request: Request) -> CsvResponse:
    """Respond with the text/csv representation for the served versions."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "/structures",
    operation_id="getOptimadeStructureList",
    summary="List all optimade structures in one query.",
    response_model=StructureResponseMany,
    response_model_exclude_unset=True,
    responses=ERROR_RESPONSES,
)
def get_structures(
    request: Request, params: EntryListingQueryParams = Depends()
) -> StructureResponseMany:
    """Retrieve a list of optimade structures by querying."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "/structures/{entry_id}",
    operation_id="getOptimadeStructure",
    summary="Get the entity of a optimade structure.",
    response_model=StructureResponseOne,
    response_model_exclude_unset=True,
    responses=ERROR_RESPONSES,
)
def get_single_structure(
    request: Request, entry_id: str, params: SingleEntryQueryParams = Depends()
) -> StructureResponseOne:
    """Get a optimade structure by querying."""
    raise HTTPException(status_code=501, detail="Not implemented.")
