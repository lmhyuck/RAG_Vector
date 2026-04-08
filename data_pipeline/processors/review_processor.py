# 2단계 : 가공 (Cleaning, Embedding)
from ai_models import embedder, llm_analyzer
import asyncio

class ReviewProcessor:
    def __init__(self):
        self.embedder = embedder
        self.llm_analyzer = llm_analyzer

    async def process_single_review(self, raw_content: str):
        """리뷰 하나를 전처리하고 벡터화함"""
        # 1. 기본적인 텍스트 정제 (특수문자 제거 등)
        clean_text = raw_content.strip().replace("\n", " ")
        
        # 2. 벡터화 (SBERT 모델 활용)
        vector = self.embedder.encode(clean_text)
        
        # 3. (선택) LLM을 통한 의도 분석 - 비용/속도를 고려해 필요시만 수행
        # analysis = await self.llm_analyzer.analyze_review(clean_text)
        
        return {
            "content": clean_text,
            "embedding": vector,
            "sentiment_score": 0.0  # 기본값, 필요시 분석 결과 대입
        }