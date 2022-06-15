import uuid
from pathlib import Path
from typing import Optional, Union

from fastapi import APIRouter, HTTPException, Request, UploadFile
from fastapi.responses import Response

from ..database import get_database
from ..models.object_storage import (
    CollectionListResponse,
    CollectionName,
    DatasetCreateResponse,
    DatasetListResponse,
    DatasetName,
)
from ..reference import object_storage

DATA_DIR = Path.cwd() / "data"


router = APIRouter(
    prefix="/data",
    responses={
        501: {"description": "Not implemented."},
    },
)


@router.get(
    "",
    operation_id="listCollections",
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
    collections = await object_storage.list_collections(get_database(), limit, offset)
    return collections or Response(status_code=204)


@router.get(
    "/{collection_name}",
    operation_id="listDatasets",
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
    try:
        datasets, headers = await object_storage.list_datasets(
            get_database(), collection_name, limit, offset
        )
        if datasets:
            return Response(
                content="{{ {} }}".format(
                    ",".join([dataset.json() for dataset in datasets])
                ),
                headers=headers,
            )
        else:
            return Response(status_code=204, headers=headers)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Collection not found.")


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
    operation_id="createCollection",
    name="Create Collection",
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
    # TODO: Support updates.
    if collection_name is None:
        collection_name = CollectionName(str(uuid.uuid4()))

    await object_storage.create_collection(
        get_database(), collection_name, request.headers
    )
    return Response(status_code=201, content=collection_name)


@router.head(
    "/{collection_name}",
    name="Get Collection Metadata",
    operation_id="getCollectionMetadata",
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
    try:
        headers = await object_storage.get_collection_metadata_headers(
            get_database(), collection_name
        )
        return Response(status_code=204, headers=headers)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Collection not found.")


@router.delete(
    "/{collection_name}",
    name="Delete Collection",
    operation_id="deleteCollection",
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
    try:
        await object_storage.delete_collection(get_database(), collection_name)
        return Response(status_code=204, content="Collection has been deleted.")
    except object_storage.ConflictError as error:
        raise HTTPException(status_code=409, detail=str(error))


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
    operation_id="createDataset",
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
    if dataset_name is None:
        dataset_name = DatasetName(str(uuid.uuid4()))

    await object_storage.create_dataset(
        get_database(),
        DATA_DIR,
        collection_name,
        dataset_name,
        file,
        dict(request.headers),
    )
    return Response(status_code=201, content=dataset_name)


@router.post(
    "/{collection_name}/",
    operation_id="createDatasetMetadata",
    name="Create Dataset Metadata",
    tags=["DataSink"],
    status_code=202,
    response_class=Response,
    responses={
        202: {"description": "Dataset metadata has been created."},
    },
)
@router.post(
    "/{collection_name}/{dataset_name}",
    operation_id="createOrReplaceDatasetMetadata",
    name="Create or Replace Dataset Metadata",
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
    operation_id="getDatasetMetadata",
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
    try:
        headers = await object_storage.get_dataset_metadata_headers(
            get_database(), collection_name, dataset_name
        )
        return Response(status_code=200, headers=headers)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not found.")


@router.get(
    "/{collection_name}/{dataset_name}",
    operation_id="getDataset",
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
    try:
        content, headers = await object_storage.get_dataset(
            get_database(), DATA_DIR, collection_name, dataset_name
        )
        return Response(content=content, headers=headers)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Not found.")


@router.delete(
    "/{collection_name}/{dataset_name}",
    operation_id="deleteDataset",
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
    await object_storage.delete_dataset(
        get_database(), DATA_DIR, collection_name, dataset_name
    )
    return Response(status_code=204)
