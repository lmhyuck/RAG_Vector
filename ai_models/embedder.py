# 텍스트를 벡터로 변환하는 로직
from sentence_transformers import SentenceTransformer
from app.core.config import settings
import numpy as np

class Embedder:
    def __init__(self):
        # 한국어 성능이 좋은 SBERT 모델 로드
        # 실무에서는 서버 기동 시 한 번만 로드하도록 설계합니다.
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL_NAME)

    def encode(self, text: str) -> np.ndarray:
        """텍스트를 벡터로 변환"""
        if not text.strip():
            raise ValueError("빈 텍스트는 인코딩할 수 없습니다.")
            
        # 벡터 생성 후 리스트 형태로 반환 (pgvector 입력 규격)
        return self.model.encode(text).tolist()

    def get_dimension(self) -> int:
        """모델의 벡터 차원 반환 (DB 설정 확인용)"""
        return self.model.get_sentence_embedding_dimension()