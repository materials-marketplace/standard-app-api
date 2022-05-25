from typing import Any, Callable, Dict, Optional

import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response

from .models import (
    DatasetCreateResponse,
    DatasetId,
    DatasetModel,
    NewTransformationModel,
    TransformationCreateResponse,
    TransformationId,
    TransformationListResponse,
    TransformationModel,
    TransformationStatusResponse,
    TransformationUpdateModel,
    TransformationUpdateResponse,
)
from .security import AuthTokenBearer
from .version import __version__


async def catch_authentication_request_errors_middleware(
    request: Request, call_next: Callable
):
    "Catch authentication requests errors to the semantic service and respond with 401."
    try:
        return await call_next(request)
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 401:
            return Response("Not authenticated.", status_code=401)
        raise


class MarketPlaceAPI(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        openapi_schema = super().openapi()
        # Example on how to add extra info to the OpenAPI schema:
        # openapi_schema["info"]["x-application-name"] = "My MarketPlace App"
        return openapi_schema


api = MarketPlaceAPI(
    title="MarketPlace Standard App API",
    description="Standard app API for the MarketPlace applications.",
    version=__version__,
    contact={
        "name": "The Materials MarketPlace Consortium",
        "url": "https://www.materials-marketplace.eu/",
        "email": "dirk.helm@iwm.fraunhofer.de",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    dependencies=[Depends(AuthTokenBearer())],
)
api.middleware("http")(catch_authentication_request_errors_middleware)


@api.get(
    "/",
    operation_id="frontend",
    tags=["FrontPage"],
    responses={
        404: {"description": "Not found."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        503: {"description": "Service unavailable."},
    },
    response_class=HTMLResponse,
)
async def frontpage() -> HTMLResponse:
    """Open the frontpage of the app."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
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


@api.post(
    "/datasets",
    operation_id="createDataset",
    tags=["DataSink"],
    response_model=DatasetCreateResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def create_dataset(dataset: DatasetModel) -> DatasetCreateResponse:
    """Create a new dataset."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/datasets/{dataset_id}",
    operation_id="getDataset",
    tags=["DataSource"],
    response_class=JSONResponse,
    response_model=DatasetModel,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_dataset(dataset_id: DatasetId) -> DatasetModel:
    """Retrieve an existing data set."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.post(
    "/transformations",
    operation_id="newTransformation",
    tags=["Transformation"],
    response_model=TransformationCreateResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def create_transformation(
    transformation: NewTransformationModel,
) -> TransformationCreateResponse:
    """Create a new transformation.

    By default when creating a new transformation resource its status is set to
    CREATED, meaning it is created on the remote system, but is not yet
    executed. To execute a transformation either set the status field directly
    to RUNNING when creating the transformation or toggle it later via the
    updateTransformation operation.

    Note that the parameters of an existing transformation can not be changed.
    """
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/transformations/{transformation_id}",
    operation_id="getTransformation",
    tags=["Transformation"],
    response_model=TransformationModel,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_transformation(
    transformation_id: TransformationId,
) -> TransformationModel:
    """Retrieve an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.delete(
    "/transformations/{transformation_id}",
    operation_id="deleteTransformation",
    tags=["Transformation"],
    status_code=204,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def delete_transformation(
    transformation_id: TransformationId,
) -> Optional[HTTPException]:
    """Delete an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.patch(
    "/transformations/{transformation_id}",
    operation_id="updateTransformation",
    tags=["Transformation"],
    response_model=TransformationUpdateResponse,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        409: {
            "description": "The requested status is unavailable (example: trying to stop an already completed transformation)."
        },
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def update_transformation(
    id: TransformationId, update: TransformationUpdateModel
) -> TransformationUpdateResponse:
    """Update an existing transformation.

    Used to change the status of a transformation. When a transformation is
    first created it is either in a CREATED or RUNNING status. The status can
    then be changed from CREATED to RUNNING or from RUNNING to STOPPED.  All
    other status update requests will result in a 409 conflict error.
    """
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/transformations/{transformation_id}/status",
    operation_id="getTransformationStatus",
    tags=["Transformation"],
    response_model=TransformationStatusResponse,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_transformation_status(
    transformation_id: TransformationId,
) -> TransformationStatusResponse:
    """Retrieve the status of a transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/transformations",
    operation_id="getTransformationList",
    tags=["Transformation"],
    response_model=TransformationListResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def list_transformation(
    limit: int = 100, offset: int = 0
) -> TransformationListResponse:
    """Retrieve a list of transformations."""
    raise HTTPException(status_code=501, detail="Not implemented.")
