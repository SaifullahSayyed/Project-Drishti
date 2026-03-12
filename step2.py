import os

with open('backend/config.py', 'w', encoding='utf-8') as f:
    f.write('''from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., min_length=1)
    REDIS_URL: str = Field(..., min_length=1)
    GROQ_API_KEY: str = Field(..., min_length=1)
    PINECONE_API_KEY: str = Field(..., min_length=1)
    PINECONE_INDEX_NAME: str = Field(..., min_length=1)
    HUGGINGFACE_TOKEN: str = Field(..., min_length=1)
    INDIAN_KANOON_API_KEY: str = Field(..., min_length=1)
    SECRET_KEY: str = Field(..., min_length=1)
    ENVIRONMENT: str = "development"
    CORS_ORIGINS: str = "http://localhost:3000,https://drishti.vercel.app"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()
''')

with open('backend/database.py', 'w', encoding='utf-8') as f:
    f.write('''from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from backend.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development"),
    future=True
)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with async_session_maker() as session:
        yield session
''')

with open('backend/models/case.py', 'w', encoding='utf-8') as f:
    f.write('''import datetime
from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from sqlalchemy.orm import relationship
from backend.database import Base

class CourtCase(Base):
    __tablename__ = "court_cases"

    id = Column(Integer, primary_key=True, index=True)
    cnr = Column(String, unique=True, index=True, nullable=False)
    case_type = Column(String, nullable=False, index=True)
    court = Column(String, nullable=False)
    district = Column(String, nullable=False, index=True)
    sections = Column(ARRAY(String), default=[])
    petitioner = Column(String)
    respondent = Column(String)
    filing_date = Column(String)
    status = Column(String)
    next_hearing = Column(String)
    data_source = Column(String)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    
    predictions = relationship("Prediction", back_populates="case", cascade="all, delete-orphan")
''')

with open('backend/models/prediction.py', 'w', encoding='utf-8') as f:
    f.write('''import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("court_cases.id"), nullable=False)
    
    petitioner_probability = Column(Float, nullable=False)
    respondent_probability = Column(Float, nullable=False)
    confidence = Column(Float, nullable=False)
    
    predicted_years = Column(Float)
    range_min = Column(Float)
    range_max = Column(Float)
    district_average = Column(Float)
    national_average = Column(Float)
    
    top_features = Column(JSON)
    data_source = Column(String)
    cases_analyzed = Column(Integer)
    
    pathway_recommended = Column(String)
    pathway_details = Column(JSON)
    
    bottlenecks = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    case = relationship("CourtCase", back_populates="predictions")
''')

with open('backend/models/__init__.py', 'w', encoding='utf-8') as f:
    f.write('''from .case import CourtCase
from .prediction import Prediction
from backend.database import Base

__all__ = ["CourtCase", "Prediction", "Base"]
''')

with open('backend/routers/cases.py', 'w', encoding='utf-8') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter(prefix="/api/case", tags=["cases"])
''')
with open('backend/routers/predict.py', 'w', encoding='utf-8') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter(prefix="/api/predict", tags=["predict"])
''')
with open('backend/routers/precedents.py', 'w', encoding='utf-8') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter(prefix="/api/precedents", tags=["precedents"])
''')
with open('backend/routers/pathway.py', 'w', encoding='utf-8') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter(prefix="/api/pathway", tags=["pathway"])
''')
with open('backend/routers/report.py', 'w', encoding='utf-8') as f:
    f.write('''from fastapi import APIRouter
router = APIRouter(prefix="/api/report", tags=["report"])
''')


with open('backend/main.py', 'w', encoding='utf-8') as f:
    f.write('''import time
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

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "message": str(exc)},
    )

app.include_router(cases.router)
app.include_router(predict.router)
app.include_router(precedents.router)
app.include_router(pathway.router)
app.include_router(report.router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}
''')

print("Step 2 basic files crafted.")
