from pydantic import BaseModel, Field
from typing import List, Optional

# 사용자가 검색할 때 보내는 양식
class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2, description="검색하고자 하는 리뷰 내용이나 의도")
    top_k: int = Field(default=5, ge=1, le=20, description="가져올 결과 개수")
    min_score: float = Field(default=0.6, description="최소 유사도 점수 (0~1)")

# 검색 결과 하나하나의 양식
class SearchResult(BaseModel):
    product_id: int
    product_name: str
    review_snippet: str
    similarity_score: float
    category: Optional[str] = "General"

# 서버가 최종적으로 응답하는 양식
class SearchResponse(BaseModel):
    results: List[SearchResult]
    execution_time: float = Field(..., description="검색에 소요된 시간 (초)")