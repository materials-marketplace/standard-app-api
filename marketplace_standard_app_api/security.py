from typing import Optional

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


class Auth(str):
    pass


class AuthTokenBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        auth = await super().__call__(request=request)
        if auth:
            return HTTPAuthorizationCredentials(
                scheme="Bearer", credentials=auth.credentials
            )
        return None
