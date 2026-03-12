from pydantic_settings import BaseSettings, SettingsConfigDict
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
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:3001,http://localhost:3002,http://localhost:3003,http://localhost:3004,https://drishti.vercel.app"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

settings = Settings()
