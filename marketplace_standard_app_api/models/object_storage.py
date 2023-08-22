from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, ConstrainedStr


class CollectionName(ConstrainedStr):
    min_length = 1
    max_length = 255


class CollectionModel(BaseModel):
    count: Optional[int]
    bytes: Optional[int]
    id: Optional[str]
    name: CollectionName
    last_modified: Optional[datetime]


class CollectionResponseModel(BaseModel):
    items: List[CollectionModel]


class CollectionCreateResponse(BaseModel):
    last_modified: datetime
    collection_id: Optional[str]


class DatasetName(ConstrainedStr):
    min_length = 1


class DatasetCreateResponse(BaseModel):
    last_modified: datetime


class DatasetModel(BaseModel):
    name: DatasetName
    hash: Optional[str]
    bytes: Optional[int]
    content_type: Optional[str]
    last_modified: Optional[datetime]


class DatasetResponseModel(BaseModel):
    items: List[DatasetModel]


class SemanticMappingName(ConstrainedStr):
    min_length = 1


class SemanticMappingModel(BaseModel):
    name: SemanticMappingName
    properties: List[Dict[str, str]]


SemanticMappingListResponse = List[SemanticMappingName]
