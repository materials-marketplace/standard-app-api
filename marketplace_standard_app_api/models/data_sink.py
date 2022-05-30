from typing import NewType

from pydantic import UUID4, BaseModel

DatasetId = NewType("DatasetId", UUID4)


class DatasetModel(BaseModel):
    pass


class DatasetCreateResponse(BaseModel):
    id: DatasetId
