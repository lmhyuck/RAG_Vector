from .collectors import BaseCollector
from .processors import ReviewProcessor
from .loaders import DBLoader

class ReviewETLPipeline:
    """수집(Extract), 가공(Transform), 적재(Load)를 총괄하는 클래스"""
    def __init__(self):
        self.collector = BaseCollector()
        self.processor = ReviewProcessor()
        self.loader = DBLoader()

    async def run_pipeline(self, product_id: int, source_url: str):
        # 1. 수집
        raw_data = self.collector.collect(source_url)
        
        # 2. 가공 (AI 모델 활용)
        processed_data = []
        for item in raw_data:
            p_data = await self.processor.process_single_review(item)
            processed_data.append(p_data)
            
        # 3. 적재 (DB 저장)
        await self.loader.load_reviews(product_id, processed_data)

__all__ = ["ReviewETLPipeline", "BaseCollector", "ReviewProcessor", "DBLoader"]