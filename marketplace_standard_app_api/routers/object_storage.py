from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import Response

from ..models.object_storage import (
    CollectionListResponse,
    CollectionName,
    DatasetCreateResponse,
    DatasetListResponse,
    DatasetName,
)

router = APIRouter(
    prefix="/data",
    responses={
        501: {"description": "Not implemented."},
    },
)


@router.get(
    "",
    operation_id="listCollections",
    summary="List all collections",
    tags=["DataSource", "DataSink"],
    response_model=CollectionListResponse,
    responses={
        204: {"description": "No collections found."},
    },
)
async def list_collections(
    limit: int = 100, offset: int = 0
) -> Union[CollectionListResponse, Response]:
    """List all collections."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "/{collection_name}",
    operation_id="listDatasets",
    summary="List all datasets in a collection",
    tags=["DataSource"],
    response_model=DatasetListResponse,
    responses={
        204: {"description": "No datasets found."},
        404: {"description": "Container not found."},
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


@router.put(
    "/{collection_name}",
    name="Create or update Collection",
    operation_id="createOrUpdateCollection",
    summary="Create or update a collection",
    tags=["DataSink"],
    status_code=201,
    response_class=Response,
    responses={
        201: {"description": "Collection has been created."},
        202: {"description": "Collection has been updated."},
        400: {"description": "Bad request."},
        507: {"description": "Insufficient storage."},
    },
    description="Create or update a collection.\n" + CREATE_COLLECTION_DESCRIPTION,
)
@router.put(
    "/",
    name="Create Collection",
    operation_id="createCollection",
    summary="Create a collection",
    tags=["DataSink"],
    status_code=201,
    response_class=Response,
    responses={
        201: {"description": "Collection has been created."},
        400: {"description": "Bad request."},
        507: {"description": "Insufficient storage."},
    },
    description="Create a collection.\n" + CREATE_COLLECTION_DESCRIPTION,
)
async def create_collection(
    request: Request, collection_name: CollectionName = None
) -> Response:
    """Create a new or replace an existing collection."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.head(
    "/{collection_name}",
    name="Get Collection Metadata",
    operation_id="getCollectionMetadata",
    summary="Get a collection's metadata",
    tags=["DataSource"],
    response_class=Response,
    status_code=204,
    responses={
        204: {"description": "Normal response."},
        404: {"description": "Not found."},
    },
)
async def get_collection_metadata(collection_name: CollectionName) -> Response:
    """Get the metadata for a collection."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.delete(
    "/{collection_name}",
    name="Delete Collection",
    operation_id="deleteCollection",
    summary="Delete an empty collection",
    tags=["DataSink"],
    response_class=Response,
    status_code=204,
    responses={
        204: {"description": "Collection has been deleted."},
        404: {"description": "Collection not found."},
        409: {"description": "Collection is not empty."},
        422: {"description": "Validation error."},
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


@router.put(
    "/{collection_name}/{dataset_name}",
    name="Create or Replace Dataset",
    operation_id="createOrReplaceDataset",
    summary="Create or replace a dataset",
    tags=["DataSink"],
    response_model=DatasetCreateResponse,
    status_code=201,
    responses={
        507: {"description": "Insufficient storage."},
    },
    description="Create or replace a dataset.\n" + CREATE_DATASET_DESCRIPTION,
)
@router.put(
    "/{collection_name}/",
    name="Create a dataset",
    operation_id="createDataset",
    summary="Create a dataset",
    tags=["DataSink"],
    response_model=DatasetCreateResponse,
    status_code=201,
    responses={
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


@router.post(
    "/{collection_name}/",
    name="Create Dataset Metadata",
    operation_id="createDatasetMetadata",
    summary="Create a dataset's metadata",
    tags=["DataSink"],
    status_code=202,
    response_class=Response,
    responses={
        202: {"description": "Dataset metadata has been created."},
    },
)
@router.post(
    "/{collection_name}/{dataset_name}",
    name="Create or Replace Dataset Metadata",
    operation_id="createOrReplaceDatasetMetadata",
    summary="Create or replace a dataset's metadata",
    tags=["DataSink"],
    status_code=202,
    response_class=Response,
    responses={
        202: {"description": "Dataset metadata has been created/updated."},
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


@router.head(
    "/{collection_name}/{dataset_name}",
    name="Get Dataset Metadata",
    operation_id="getDatasetMetadata",
    summary="Get a dataset's metadata",
    tags=["DataSource"],
    status_code=200,
    response_class=Response,
    responses={
        404: {"description": "Not found."},
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


@router.get(
    "/{collection_name}/{dataset_name}",
    name="Get Dataset",
    operation_id="getDataset",
    summary="Get a dataset",
    tags=["DataSource"],
    response_class=Response,
    responses={
        404: {"description": "Not found."},
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


@router.delete(
    "/{collection_name}/{dataset_name}",
    name="Delete Dataset",
    operation_id="deleteDataset",
    summary="Delete a dataset",
    tags=["DataSink"],
    status_code=204,
    responses={
        404: {"description": "Not found."},
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
