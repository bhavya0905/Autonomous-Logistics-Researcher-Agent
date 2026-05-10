import os
from dotenv import load_dotenv
load_dotenv()
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    OPENAI_API_KEY: str | None = None
    GROQ_API_KEY: str | None = None
    TAVILY_API_KEY: str | None = None

    MODEL_NAME: str = "llama-3.3-70b-versatile"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

    VECTOR_DB_PATH: str = "memory/chroma_db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings():
    return Settings()