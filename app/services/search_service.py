import time
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from database.vector_store import VectorStore

class SearchService:
    def __init__(self, db: AsyncSession, embedder):
        self.db = db
        self.vector_store = VectorStore(db)
        self.embedder = embedder

    async def perform_semantic_search(self, request: SearchRequest) -> SearchResponse:
        start_time = time.time()
        
        # 1. 쿼리 임베딩 생성
        query_vector = self.embedder.encode(request.query)
        
        # 2. Vector DB에서 유사도 검색 수행
        raw_results = await self.vector_store.search_similarity(
            query_vector=query_vector,
            limit=request.top_k,
            threshold=request.min_score
        )
        
        # 3. 결과를 Pydantic 모델 형식으로 변환
        processed_results = []
        for row in raw_results:
            processed_results.append(SearchResult(
                product_id=row.product_id,
                product_name="임시 상품명", # 실제로는 Join 쿼리로 가져옴
                review_snippet=row.content,
                similarity_score=round(float(row.score), 4),
                category="General"
            ))
            
        execution_time = time.time() - start_time
        
        return SearchResponse(
            results=processed_results,
            execution_time=round(execution_time, 3)
        )