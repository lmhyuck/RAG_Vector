from pydantic_settings import BaseSettings
from typing import List, Union
import json

class Settings(BaseSettings):
    # Project Info
    PROJECT_NAME: str = "Review-Sense API"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    # .env에서 DATABASE_URL을 읽어오며, 기본값을 설정할 수 있습니다.
    DATABASE_URL: str
    
    # AI Model Settings
    EMBEDDING_MODEL_NAME: str = "snunlp/KR-SBERT-V4-any-precision"
    OPENAI_API_KEY: str
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: str  # 일단 글자로 가져옴

    # 나중에 쓸 때 리스트로 바꿔서 내보내는 프로퍼티
    @property
    def cors_origins_list(self) -> list:
        return self.BACKEND_CORS_ORIGINS.split(",")

settings = Settings()