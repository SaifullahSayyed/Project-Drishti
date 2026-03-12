import time
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.config import settings
from backend.database import engine, Base
from backend.routers import cases, predict, precedents, pathway, report

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), "INFO"))
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup
    async with engine.begin() as conn:
        logger.info("Creating database tables if not exist...")
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Cleanup on shutdown
    logger.info("Shutting down...")

app = FastAPI(title="DRISHTI API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request started: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(f"Request completed: {request.method} {request.url.path} in {process_time:.4f}s with status {response.status_code}")
        response.headers["X-Process-Time"] = str(process_time)
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(f"Request failed: {request.method} {request.url.path} in {process_time:.4f}s with error: {str(e)}")
        raise e

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from backend.error_handlers import custom_http_exception_handler, validation_exception_handler, global_exception_handler

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(cases.router)
app.include_router(predict.router)
app.include_router(precedents.router)
app.include_router(pathway.router)
app.include_router(report.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
