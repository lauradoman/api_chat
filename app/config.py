
from pydantic import BaseSettings

class Settings(BaseSettings):
    port: int = 8000
    max_history: int = 5
    max_response_time: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
