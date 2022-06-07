from datetime import datetime
from typing import NewType

from pydantic import UUID4, BaseModel

DatasetId = NewType("DatasetId", UUID4)


class DatasetCreateResponse(BaseModel):
    last_modified: datetime
