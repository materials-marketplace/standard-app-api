from typing import Any, Callable, Dict, Optional, Union

import requests
from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response

from .models.object_storage import (
    CollectionListResponse,
    CollectionName,
    DatasetCreateResponse,
    DatasetListResponse,
    DatasetName,
)
from .models.system import GlobalSearchResponse
from .models.transformation import (
    NewTransformationModel,
    TransformationCreateResponse,
    TransformationId,
    TransformationListResponse,
    TransformationModel,
    TransformationStateResponse,
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


@api.get(
    "/data",
    operation_id="listCollections",
    tags=["DataSource", "DataSink"],
    response_model=CollectionListResponse,
    responses={
        204: {"description": "No collections found."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def list_collections(
    limit: int = 100, offset: int = 0
) -> Union[CollectionListResponse, Response]:
    """List all collections."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/data/{collection_name}",
    operation_id="listDatasets",
    tags=["DataSource"],
    response_model=DatasetListResponse,
    responses={
        204: {"description": "No datasets found."},
        401: {"description": "Not authenticated."},
        404: {"description": "Container not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def list_datasets(
    collection_name: CollectionName, limit: int = 100, offset: int = 0
) -> Union[DatasetListResponse, Response]:
    """List all datasets."""
    raise HTTPException(status_code=501, detail="Not implemented.")


CREATE_COLLECTION_DESCRIPTION = """
To add custom metadata, add keys to the header of the form:

- X-Object-Meta-name: value

Where 'name' is the name of the metadata key and 'value' is the
corresponding value.

Note: This operation is in compliance with the OpenStack Swift object
storage API:
https://docs.openstack.org/api-ref/object-store/index.html#create-container
"""


@api.put(
    "/data/{collection_name}",
    name="Create or update Collection",
    operation_id="createOrUpdateCollection",
    tags=["DataSink"],
    status_code=201,
    response_class=Response,
    responses={
        201: {"description": "Collection has been created."},
        202: {"description": "Collection has been updated."},
        400: {"description": "Bad request."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
        507: {"description": "Insufficient storage."},
    },
    description="Create or update a collection.\n" + CREATE_COLLECTION_DESCRIPTION,
)
@api.put(
    "/data/",
    operation_id="createCollection",
    name="Create Collection",
    tags=["DataSink"],
    status_code=201,
    response_class=Response,
    responses={
        201: {"description": "Collection has been created."},
        400: {"description": "Bad request."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
        507: {"description": "Insufficient storage."},
    },
    description="Create a collection.\n" + CREATE_COLLECTION_DESCRIPTION,
)
async def create_collection(
    request: Request, collection_name: CollectionName = None
) -> Response:
    """Create a new or replace an existing collection."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.head(
    "/data/{collection_name}",
    name="Get Collection Metadata",
    operation_id="getCollectionMetadata",
    tags=["DataSource"],
    response_class=Response,
    status_code=204,
    responses={
        204: {"description": "Normal response."},
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_collection_metadata(collection_name: CollectionName) -> Response:
    """Get the metadata for a collection."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.delete(
    "/data/{collection_name}",
    name="Delete Collection",
    operation_id="deleteCollection",
    tags=["DataSink"],
    response_class=Response,
    status_code=204,
    responses={
        204: {"description": "Collection has been deleted."},
        401: {"description": "Not authenticated."},
        404: {"description": "Collection not found."},
        409: {"description": "Collection is not empty."},
        422: {"description": "Validation error."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def delete_collection(collection_name: CollectionName) -> Response:
    """Delete an empty collection."""
    raise HTTPException(status_code=501, detail="Not implemented.")


CREATE_DATASET_DESCRIPTION = """
To add custom metadata, add keys to the header of the form:

- X-Object-Meta-name: value

Where 'name' is the name of the metadata key and 'value' is the
corresponding value.

Note: This operation is in compliance with the OpenStack Swift object
storage API:
https://docs.openstack.org/api-ref/object-store/index.html#create-or-replace-object
"""


@api.put(
    "/data/{collection_name}/{dataset_name}",
    name="Create or Replace Dataset",
    operation_id="createOrReplaceDataset",
    tags=["DataSink"],
    response_model=DatasetCreateResponse,
    status_code=201,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
        507: {"description": "Insufficient storage."},
    },
    description="Create or replace a dataset.\n" + CREATE_DATASET_DESCRIPTION,
)
@api.put(
    "/data/{collection_name}/",
    operation_id="createDataset",
    tags=["DataSink"],
    response_model=DatasetCreateResponse,
    status_code=201,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
        507: {"description": "Insufficient storage."},
    },
    description="Create a dataset.\n" + CREATE_DATASET_DESCRIPTION,
)
async def create_dataset(
    request: Request,
    file: UploadFile,
    collection_name: CollectionName,
    dataset_name: Optional[DatasetName] = None,
) -> Union[DatasetCreateResponse, Response]:
    """Create a new or replace an existing dataset."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.post(
    "/data/{collection_name}/",
    operation_id="createDatasetMetadata",
    name="Create Dataset Metadata",
    tags=["DataSink"],
    status_code=202,
    response_class=Response,
    responses={
        202: {"description": "Dataset metadata has been created."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
@api.post(
    "/data/{collection_name}/{dataset_name}",
    operation_id="createOrReplaceDatasetMetadata",
    name="Create or Replace Dataset Metadata",
    tags=["DataSink"],
    status_code=202,
    response_class=Response,
    responses={
        202: {"description": "Dataset metadata has been created/updated."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def create_or_replace_dataset_metadata(
    collection_name: CollectionName,
    dataset_name: Optional[DatasetName] = None,
) -> Response:
    """Create or replace dataset metadata.

    Note: This operation is in compliance with the OpenStack Swift object
    storage API:
    https://docs.openstack.org/api-ref/object-store/index.html#create-or-update-object-metadata
    """
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.head(
    "/data/{collection_name}/{dataset_name}",
    operation_id="getDatasetMetadata",
    tags=["DataSource"],
    status_code=200,
    response_class=Response,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_dataset_metadata(
    collection_name: CollectionName, dataset_name: DatasetName
) -> Response:
    """Get dataset metadata.

    Returns the dataset metadata in the response header in the form of:

    - X-Object-Meta-name: value

    Where 'name' is the name of the metadata key and 'value' is the
    corresponding value.

    Example response header for a plain-text file:
    - Content-Type: text/plain;charset=UTF-8
    - Content-Length: 1234
    - X-Object-Meta-my-key: some-value

    Note: This operation is in compliance with the OpenStack Swift object
    storage API:
    https://docs.openstack.org/api-ref/object-store/index.html#show-object-metadata
    """
    # return Response(content=None, headers={"X-Object-Meta-my-key": "some-value"})
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/data/{collection_name}/{dataset_name}",
    operation_id="getDataset",
    tags=["DataSource"],
    response_class=Response,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_dataset(
    collection_name: CollectionName, dataset_name: DatasetName
) -> Response:
    """Get a dataset.

    Returns the object as part of the request body and metadata as part of the
    response headers.

    In addition to the standard response header keys (Content-Type and
    Content-Length), the header may also contain metadata key-value pairs in the
    form of:

    - X-Object-Meta-name: value

    Where 'name' is the name of the metadata key and 'value' is the
    corresponding value.

    Example response header for a plain-text file:
    - Content-Type: text/plain;charset=UTF-8
    - Content-Length: 1234
    - X-Object-Meta-my-key: some-value

    Note: This operation is in compliance with the OpenStack Swift object
    storage API:
    https://docs.openstack.org/api-ref/object-store/index.html#get-object-content-and-metadata
    """
    # return Response(content=data, headers={"X-Object-Meta-my-key": "some-value"})
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.delete(
    "/data/{collection_name}/{dataset_name}",
    operation_id="deleteDataset",
    tags=["DataSink"],
    status_code=204,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def delete_dataset(
    collection_name: CollectionName, dataset_name: DatasetName
) -> Response:
    """Delete a dataset with the given dataset id.

    Note: This operation is in compliance with the OpenStack Swift object
    storage API:
    https://docs.openstack.org/api-ref/object-store/index.html#delete-object
    """
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

    By default when creating a new transformation resource its state is set to
    CREATED, meaning it is created on the remote system, but is not yet
    executed. To execute a transformation either set the state field directly to
    RUNNING when creating the transformation or toggle it later via the
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
            "description": "The requested state is unavailable (example: trying to stop an already completed transformation)."
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

    Used to change the state of a transformation. When a transformation is first
    created it is either in a CREATED or RUNNING state. The state can then be
    changed from CREATED to RUNNING or from RUNNING to STOPPED.  All other state
    update requests will result in a 409 conflict error.
    """
    raise HTTPException(status_code=501, detail="Not implemented.")


@api.get(
    "/transformations/{transformation_id}/state",
    operation_id="getTransformationState",
    tags=["Transformation"],
    response_model=TransformationStateResponse,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_transformation_state(
    transformation_id: TransformationId,
) -> TransformationStateResponse:
    """Retrieve the state of a transformation."""
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
