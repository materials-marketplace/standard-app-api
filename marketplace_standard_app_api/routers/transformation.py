from dataclasses import asdict
from uuid import UUID

from fastapi import APIRouter, HTTPException, Response

from ..models.transformation import (
    NewTransformationModel,
    TransformationCreateResponse,
    TransformationId,
    TransformationListResponse,
    TransformationModel,
    TransformationState,
    TransformationStateResponse,
    TransformationUpdateModel,
    TransformationUpdateResponse,
)
from ..reference.simulation_controller import Simulation, SimulationManager

simulation_manager = SimulationManager()


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
    transformation_id = TransformationId(
        UUID(simulation_manager.create_simulation(transformation.parameters))
    )
    return TransformationCreateResponse(id=transformation_id)


@router.get(
    "/{transformation_id}",
    operation_id="getTransformation",
    response_model=TransformationModel,
    responses={
        404: {"description": "Not found."},
    },
)
async def get_transformation(
    transformation_id: TransformationId,
) -> TransformationModel:
    """Retrieve an existing transformation."""
    try:
        simulation = simulation_manager._get_simulation(str(transformation_id))
    except KeyError:
        raise HTTPException(404, "Not found.")
    status = simulation_manager.get_simulation_state(job_id=str(transformation_id))
    return TransformationModel(
        id=transformation_id,
        parameters=asdict(simulation.config),
        state=status.name,
    )


@router.delete(
    "/{transformation_id}",
    operation_id="deleteTransformation",
    status_code=204,
    responses={
        404: {"description": "Not found."},
    },
)
async def delete_transformation(
    transformation_id: TransformationId,
) -> Response:
    """Delete an existing transformation."""
    try:
        simulation_manager.delete_simulation(job_id=str(transformation_id))
        return Response(status_code=204)
    except KeyError:
        raise HTTPException(404, "Not found.")


@router.patch(
    "/{transformation_id}",
    operation_id="updateTransformation",
    response_model=TransformationUpdateResponse,
    responses={
        404: {"description": "Not found."},
        409: {
            "description": "The requested state is unavailable (example: trying to stop an already completed transformation)."
        },
    },
)
async def update_transformation(
    transformation_id: TransformationId, update: TransformationUpdateModel
) -> TransformationUpdateResponse:
    """Update an existing transformation.

    Used to change the state of a transformation. When a transformation is first
    created it is either in a CREATED or RUNNING state. The state can then be
    changed from CREATED to RUNNING or from RUNNING to STOPPED.  All other state
    update requests will result in a 409 conflict error.
    """
    try:
        status = simulation_manager.get_simulation_state(job_id=str(transformation_id))
    except KeyError:
        raise HTTPException(404, "Not found.")
    if update.state is TransformationState.RUNNING and status.name == "CREATED":
        simulation_manager.run_simulation(job_id=str(transformation_id))
        return TransformationUpdateResponse(id=transformation_id, state=update.state)
    elif update.state is TransformationState.STOPPED and status.name == "RUNNING":
        simulation_manager.stop_simulation(job_id=str(transformation_id))
        return TransformationUpdateResponse(id=transformation_id, state=update.state)

    raise HTTPException(409, "The requested state is unavailable.")


@router.get(
    "/{transformation_id}/state",
    operation_id="getTransformationState",
    response_model=TransformationStateResponse,
    responses={
        404: {"description": "Not found."},
    },
)
async def get_transformation_state(
    transformation_id: TransformationId,
) -> TransformationStateResponse:
    """Retrieve the state of a transformation."""
    try:
        status = simulation_manager.get_simulation_state(job_id=str(transformation_id))
        return TransformationStateResponse(id=transformation_id, state=status.name)
    except KeyError:
        raise HTTPException(404, "Not found.")


@router.get(
    "",
    operation_id="getTransformationList",
    response_model=TransformationListResponse,
)
async def list_transformation(
    limit: int = 100, offset: int = 0
) -> TransformationListResponse:
    """Retrieve a list of transformations."""
    simulation_ids = simulation_manager.get_simulation_list()[offset : offset + limit]
    simulations: list[Simulation] = [
        simulation_manager._get_simulation(sim_id) for sim_id in simulation_ids
    ]

    return TransformationListResponse(
        items=[
            TransformationModel(
                id=simulation.job_id, parameters=asdict(simulation.config)
            )
            for simulation in simulations
        ]
    )
