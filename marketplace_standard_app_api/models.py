from enum import Enum
from typing import Literal, NewType, TypeAlias

from pydantic import UUID4, BaseModel

ApplicationId = NewType("ApplicationId", UUID4)


DatasetId = NewType("DatasetId", UUID4)


class DatasetModel(BaseModel):
    pass


class DatasetCreateResponse(BaseModel):
    id: DatasetId


TransformationId = NewType("TransformationId", UUID4)


class TransformationStatus(str, Enum):
    # The following statuses can be set by the user:
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    STOPPED = "STOPPED"

    # The following statuses can only be set by the application:
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class NewTransformationModel(BaseModel):
    parameters: dict

    # When creating a new transformation, the default status is CREATED, but the
    # user can request it to be changed to RUNNING immediately.
    status: Literal[
        TransformationStatus.CREATED, TransformationStatus.RUNNING
    ] = TransformationStatus.CREATED


class TransformationCreateResponse(BaseModel):
    id: TransformationId


class TransformationModel(BaseModel):
    id: TransformationId
    parameters: dict
    status: TransformationStatus | None = None


# When updating a transformation, the status can be toggled between RUNNING and
# STOPPED.
UpdateTransformationStates: TypeAlias = Literal[
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
    items: list[TransformationModel]
