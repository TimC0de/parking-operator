import logging

from contextlib import asynccontextmanager

from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse

from app.api.routers.api import api_router
from fastapi.encoders import jsonable_encoder

from app.config.logging import setup_logging

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


# Setup logging
setup_logging()


#  Define the app (this should be readed from another file)
app = FastAPI(
    title="Parking Assistant Backend",
    version="0.0.1",
    docs_url="/docs",
    openapi_url="/api/docs/openapi.json",
    redoc_url="/documentation",  # Enhable Redoc UI,
    lifespan=lifespan
)


# Include the routers
app.include_router(api_router)


@app.exception_handler(status.HTTP_500_INTERNAL_SERVER_ERROR)
async def error_500(_: Request, error: HTTPException):
    """
    TODO: Handle the error with our own error handling system.
    """
    log.error(
        "500 - Internal Server Error",
        exc_info=(type(error), error, error.__traceback__),
    )

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Server got itself in trouble",
        },
    )


from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"],
)
