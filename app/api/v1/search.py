import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import Optional
from sentence_transformers import SentenceTransformer

from database.connection import AsyncSessionLocal

class SearchRequest(BaseModel):
    query: str
    top_k: Optional[int] = 5
    min_score: Optional[float] = 0.6

router = APIRouter()
model = SentenceTransformer('jhgan/ko-sroberta-multitask')

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/search")
async def search_reviews(request: SearchRequest, db: AsyncSession = Depends(get_db)):
    try:
        # 1. 벡터 생성 및 리스트를 '쉼표로 구분된 문자열'로 변환
        # [0.1, 0.2] -> "0.1, 0.2" (대괄호를 아예 제거해서 드라이버의 자동 변환을 방지)
        query_vector = model.encode(request.query).tolist()
        vector_plain_str = ",".join(map(str, query_vector))

        # 2. SQL 쿼리 수정
        # 문자열을 중괄호 {}로 감싸서 PostgreSQL의 배열(Array) 텍스트 형식으로 만든 뒤 vector로 캐스팅
        query = text("""
            SELECT 
                r.product_id, 
                p.name as product_name,
                r.content, 
                1 - (r.embedding <=> ('[' || :vector_str || ']')::vector) AS score
            FROM reviews r
            JOIN products p ON r.product_id = p.id
            WHERE 1 - (r.embedding <=> ('[' || :vector_str || ']')::vector) > :min_score
            ORDER BY score DESC
            LIMIT :limit
        """)

        result = await db.execute(
            query, 
            {
                "vector_str": vector_plain_str, # "[...]"가 아니라 "0.1, 0.2..." 형태
                "min_score": request.min_score,
                "limit": request.top_k
            }
        )
        
        search_results = []
        for row in result:
            search_results.append({
                "product_id": row.product_id,
                "product_name": row.product_name,
                "content": row.content,
                "score": round(float(row.score), 4)
            })

        return {"results": search_results}

    except Exception as e:
        print(f"DEBUG: {str(e)}")
        raise HTTPException(status_code=500, detail=f"검색 오류: {str(e)}")