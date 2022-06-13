from datetime import datetime
from typing import List, NewType, Optional

from pydantic import UUID4, BaseModel, ConstrainedStr


class CollectionName(ConstrainedStr):
    min_length = 1
    max_length = 255


class CollectionListItemModel(BaseModel):
    count: int
    bytes: int
    name: CollectionName
    last_modified: Optional[datetime]


CollectionListResponse = List[CollectionListItemModel]


DatasetId = NewType("DatasetId", UUID4)


class DatasetCreateResponse(BaseModel):
    last_modified: datetime


class DatasetModel(BaseModel):
    id: DatasetId
    hash: Optional[str]
    bytes: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]


DatasetListResponse = List[DatasetModel]
