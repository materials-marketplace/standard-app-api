from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field


class GlobalSearchResponseItemModel(BaseModel):
    """Default query reply model"""

    label: Optional[str] = Field(
        None, description="Short label describing the search result"
    )
    description: Optional[str] = Field(
        None, description="Short label describing the search result"
    )
    url: Optional[AnyUrl] = Field(None, description="URL to search results")
    score: Optional[float] = Field(
        None,
        description=(
            "Semantic relevance of search result. "
            "Can be used to infer the ordering of search result"
        ),
    )


# TODO: See below for an alternative definition.
GlobalSearchResponse = List[GlobalSearchResponseItemModel]

# TODO: I think we should deprecate the direct exposure of the items and instead
# return them as part of an object similar to the transformationList response.
# class GlobalSearchResponse(BaseModel):
#     items: List[GlobalSearchResponseItemModel]
