# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GOOGLE_API_KEY: str
    GEMINI_MODEL_NAME: str ="gemini-2.5-flash"
    OPENAI_MODEL_NAME: str = "gpt-4o"
    REDIS_URL: str = "redis://localhost:6379"
    port: int = 8000
    max_history: int = 5
    max_response_time: int = 30

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
