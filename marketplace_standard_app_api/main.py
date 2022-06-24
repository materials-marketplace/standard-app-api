from typing import Any, Callable, Dict

import requests
from fastapi import Depends, FastAPI, Request
from fastapi.responses import Response

from .routers import frontend, object_storage, system, transformation
from .security import AuthTokenBearer
from .version import __version__


async def catch_authentication_request_errors_middleware(
    request: Request, call_next: Callable
):
    "Catch authentication requests errors to the semantic service and respond with 401."
    try:
        return await call_next(request)
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 401:
            return Response("Not authenticated.", status_code=401)
        raise


class MarketPlaceAPI(FastAPI):
    def openapi(self) -> Dict[str, Any]:
        openapi_schema = super().openapi()
        # Example on how to add extra info to the OpenAPI schema:
        # openapi_schema["info"]["x-application-name"] = "My MarketPlace App"
        return openapi_schema


api = MarketPlaceAPI(
    title="MarketPlace Standard App API",
    description="Standard app API for the MarketPlace applications.",
    version=__version__,
    contact={
        "name": "The Materials MarketPlace Consortium",
        "url": "https://www.materials-marketplace.eu/",
        "email": "dirk.helm@iwm.fraunhofer.de",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    dependencies=[Depends(AuthTokenBearer())],
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        503: {"description": "Service unavailable."},
    },
)
api.middleware("http")(catch_authentication_request_errors_middleware)

api.include_router(frontend.router)
api.include_router(system.router)
api.include_router(object_storage.router)
api.include_router(transformation.router)
