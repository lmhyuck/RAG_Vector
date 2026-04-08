# pgvector 전용 쿼리 및 HNSW 인덱스 관리
## HNSW : 벡터 데이터에서 근사 최근접 이웃 탐색(ANN) 탐색 수행하기 위한 알고리즘

from sqlalchemy import text
from database.connection import engine

class VectorStore:
    def __init__(self, session):
        self.session = session

    async def search_similarity(self, query_vector, limit=5, threshold=0.7):
        """
        [Search 전용] 사용자의 질문 벡터와 가장 유사한 리뷰를 검색
        """
        query = text("""
            SELECT product_id, content, 1 - (embedding <=> :q) AS score
            FROM reviews
            WHERE 1 - (embedding <=> :q) > :threshold
            ORDER BY score DESC
            LIMIT :limit
        """)
        
        result = await self.session.execute(
            query, {"q": query_vector, "limit": limit, "threshold": threshold}
        )
        return result.fetchall()