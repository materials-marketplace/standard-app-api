from enum import Enum
from typing import List, Literal, NewType, Optional

from pydantic import UUID4, BaseModel

ApplicationId = NewType("ApplicationId", UUID4)

TransformationId = NewType("TransformationId", UUID4)


class TransformationState(str, Enum):
    # The following states can be set by the user:
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"

    # The following states can only be set by the application:
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# TODO (py310): Use TypeAlias to explcitly define the type.
NewTransformationStates = Literal[
    TransformationState.CREATED, TransformationState.RUNNING
]


class NewTransformationModel(BaseModel):
    parameters: dict

    # When creating a new transformation, the default state is CREATED, but the
    # user can request it to be changed to RUNNING immediately.
    state: NewTransformationStates = TransformationState.CREATED


class TransformationCreateResponse(BaseModel):
    id: TransformationId


class TransformationModel(BaseModel):
    id: TransformationId
    parameters: dict
    state: Optional[TransformationState] = None


# When updating a transformation, the state can be toggled between RUNNING and
# STOPPED.
# TODO (py310): Use TypeAlias to explcitly define the type.
UpdateTransformationStates = Literal[
    TransformationState.RUNNING, TransformationState.STOPPED
]


class TransformationUpdateModel(BaseModel):
    state: UpdateTransformationStates


class TransformationUpdateResponse(BaseModel):
    id: TransformationId
    state: UpdateTransformationStates


class TransformationStateResponse(BaseModel):
    id: TransformationId
    state: TransformationState


class TransformationListResponse(BaseModel):
    items: List[TransformationModel]
