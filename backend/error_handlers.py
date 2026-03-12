import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)

async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP exception: {exc.detail} on path {request.url.path}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": True, "message": exc.detail, "path": request.url.path},
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(f"Validation error: {exc.errors()} on path {request.url.path}")
    return JSONResponse(
        status_code=422,
        content={"error": True, "message": "Invalid input data", "details": exc.errors()},
    )

async def global_exception_handler(request: Request, exc: Exception):
    logger.critical(f"Unhandled exception: {str(exc)} on path {request.url.path}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "An unexpected internal error occurred in DRISHTI."},
    )
