from typing import Dict, Optional

from pydantic import BaseModel, Field


class MessageBrokerRequestModel(BaseModel):
    endpoint: str = Field("", description="API endpoint of the application")
    query_params: Optional[Dict[str, str]] = Field(None, description="Query parameters")
    headers: Optional[Dict[str, str]] = Field(None, description="Request headers")
    method: str = Field("", description="The HTTP request method")
    body: Optional[str] = Field(None, description="The request message body")


class MessageBrokerResponseModel(BaseModel):
    status_code: int = Field(200, description="The HTTP response code")
    headers: Optional[Dict[str, str]] = Field(None, description="Response headers")
    body: Optional[str] = Field(None, description="The response message body")
