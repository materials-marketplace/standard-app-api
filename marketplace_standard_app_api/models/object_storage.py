from datetime import datetime
from typing import List, NewType, Optional

from pydantic import UUID4, BaseModel

DatasetId = NewType("DatasetId", UUID4)


class DatasetCreateResponse(BaseModel):
    last_modified: datetime


class DatasetModel(BaseModel):
    id: DatasetId
    hash: Optional[str]
    bytes: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]


class DatasetListResponse(BaseModel):
    items: List[DatasetModel]
