from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .data_sink import DatasetId


class DatasetModel(BaseModel):
    id: DatasetId
    hash: Optional[str]
    bytes: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]


class DatasetListResponse(BaseModel):
    items: List[DatasetModel]
