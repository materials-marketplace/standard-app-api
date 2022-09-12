from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(
    prefix="/optimade",
    tags=["Optimade"],
    responses={
        501: {"description": "Not implemented"},
    },
)
