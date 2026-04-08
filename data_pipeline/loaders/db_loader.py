# 3단계 : 적재( Bulk Load)
from sqlalchemy.future import select
from database.connection import AsyncSessionLocal
from database.models import Product, Review

class DBLoader:
    def __init__(self, session_factory=AsyncSessionLocal):
        self.session_factory = session_factory

    async def load_reviews(self, product_id: int, processed_data_list: list):
        """가공된 리뷰 리스트를 DB에 일괄 저장"""
        async with self.session_factory() as session:
            async with session.begin():
                for data in processed_data_list:
                    new_review = Review(
                        product_id=product_id,
                        content=data["content"],
                        embedding=data["embedding"],
                        sentiment_score=data["sentiment_score"]
                    )
                    session.add(new_review)
            # transaction 종료 시 자동 commit
            print(f"{len(processed_data_list)} 건의 리뷰 적재 완료.")