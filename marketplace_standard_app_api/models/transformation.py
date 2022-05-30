from enum import Enum
from typing import List, Literal, NewType, Optional

from pydantic import UUID4, BaseModel

ApplicationId = NewType("ApplicationId", UUID4)

TransformationId = NewType("TransformationId", UUID4)


class TransformationStatus(str, Enum):
    # The following statuses can be set by the user:
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"

    # The following statuses can only be set by the application:
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


# TODO (py310): Use TypeAlias to explcitly define the type.
NewTransformationStates = Literal[
    TransformationStatus.CREATED, TransformationStatus.RUNNING
]


class NewTransformationModel(BaseModel):
    parameters: dict

    # When creating a new transformation, the default status is CREATED, but the
    # user can request it to be changed to RUNNING immediately.
    status: NewTransformationStates = TransformationStatus.CREATED


class TransformationCreateResponse(BaseModel):
    id: TransformationId


class TransformationModel(BaseModel):
    id: TransformationId
    parameters: dict
    status: Optional[TransformationStatus] = None


# When updating a transformation, the status can be toggled between RUNNING and
# STOPPED.
# TODO (py310): Use TypeAlias to explcitly define the type.
UpdateTransformationStates = Literal[
    TransformationStatus.RUNNING, TransformationStatus.STOPPED
]


class TransformationUpdateModel(BaseModel):
    status: UpdateTransformationStates


class TransformationUpdateResponse(BaseModel):
    id: TransformationId
    status: UpdateTransformationStates


class TransformationStatusResponse(BaseModel):
    id: TransformationId
    status: TransformationStatus


class TransformationListResponse(BaseModel):
    items: List[TransformationModel]
