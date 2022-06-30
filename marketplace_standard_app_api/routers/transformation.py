from typing import Optional

from fastapi import APIRouter, HTTPException

from ..models.transformation import (
    NewTransformationModel,
    TransformationCreateResponse,
    TransformationId,
    TransformationListResponse,
    TransformationModel,
    TransformationStateResponse,
    TransformationUpdateModel,
    TransformationUpdateResponse,
)

router = APIRouter(
    prefix="/transformations",
    tags=["Transformation"],
    responses={
        501: {"description": "Not implemented."},
    },
)


@router.post(
    "",
    operation_id="newTransformation",
    summary="Create a new transformation",
    response_model=TransformationCreateResponse,
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


@router.get(
    "/{transformation_id}",
    operation_id="getTransformation",
    summary="Get a transformation",
    response_model=TransformationModel,
    responses={
        404: {"description": "Not found."},
    },
)
async def get_transformation(
    transformation_id: TransformationId,
) -> TransformationModel:
    """Retrieve an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.delete(
    "/{transformation_id}",
    operation_id="deleteTransformation",
    summary="Delete a transformation",
    status_code=204,
    responses={
        404: {"description": "Not found."},
    },
)
async def delete_transformation(
    transformation_id: TransformationId,
) -> Optional[HTTPException]:
    """Delete an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.patch(
    "/{transformation_id}",
    operation_id="updateTransformation",
    summary="Update a transformation",
    response_model=TransformationUpdateResponse,
    responses={
        404: {"description": "Not found."},
        409: {
            "description": "The requested state is unavailable (example: trying to stop an already completed transformation)."
        },
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


@router.get(
    "/{transformation_id}/state",
    operation_id="getTransformationState",
    summary="Get the state of a transformation",
    response_model=TransformationStateResponse,
    responses={
        404: {"description": "Not found."},
    },
)
async def get_transformation_state(
    transformation_id: TransformationId,
) -> TransformationStateResponse:
    """Retrieve the state of a transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@router.get(
    "",
    operation_id="getTransformationList",
    summary="List all transformations",
    response_model=TransformationListResponse,
)
async def list_transformation(
    limit: int = 100, offset: int = 0
) -> TransformationListResponse:
    """Retrieve a list of transformations."""
    raise HTTPException(status_code=501, detail="Not implemented.")
