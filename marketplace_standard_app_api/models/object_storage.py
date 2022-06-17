from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConstrainedStr


class CollectionName(ConstrainedStr):
    min_length = 1
    max_length = 255


class CollectionListItemModel(BaseModel):
    count: int
    bytes: int
    name: CollectionName
    last_modified: Optional[datetime]


CollectionListResponse = List[CollectionListItemModel]


class DatasetName(ConstrainedStr):
    min_length = 1


class DatasetCreateResponse(BaseModel):
    last_modified: datetime


class DatasetModel(BaseModel):
    id: DatasetName
    hash: Optional[str]
    bytes: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]


DatasetListResponse = List[DatasetModel]
