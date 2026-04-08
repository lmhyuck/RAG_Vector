# 리뷰 요약 및 의도 추출 (GPT/Llama 등 활용)
from openai import AsyncOpenAI
from app.core.config import settings

class LLMAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_review(self, content: str) -> dict:
        """리뷰에서 구매 의도 및 핵심 키워드 추출"""
        prompt = f"""
        다음 리뷰를 분석하여 1) 핵심 요약 2) 구매 의도(선물, 가성비, 성능 등) 
        3) 감성 점수(-1~1)를 JSON 형식으로 응답해줘.
        리뷰 내용: {content}
        """
        
        response = await self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        # LLM 결과를 파이프라인에서 메타데이터로 활용
        return response.choices[0].message.content