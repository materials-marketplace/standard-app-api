from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class MessageBrokerRequestModel(BaseModel):
    endpoint: str = Field(None, description="API endpoint of the application")
    body_base64: str = Field(None, description="A base64-encrypted body")
    body: Optional[Any] = Field(None, description="The request message payload")
    query_params: Optional[Dict[str, str]] = Field(None, description="Query parameters")
    headers: Optional[Dict[str, str]] = Field(None, description="Request headers")


class MessageBrokerResponseModel(BaseModel):
    status_code: int = Field(200, description="The HTTP response code")
    body_base64: str = Field(None, description="A base64-encrypted body")
    body: Optional[Any] = Field(None, description="The response message payload")
    headers: Optional[Dict[str, str]] = Field(None, description="Response headers")
