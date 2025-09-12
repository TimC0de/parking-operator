from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.api.routers import resolve

api_router = APIRouter()
api_router.prefix = "/api"
api_router.default_response_class = JSONResponse


api_router.include_router(resolve.router, prefix="/resolve", tags=["Resolve"])