import asyncio
import sys
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from database.connection import Base
from app.core.config import settings
# 모델들이 임포트되어야 Base.metadata가 인식함
from database.models.product import Product
from database.models.review import Review
from database.vector_store import VectorStore

async def init_db():
    print("🚀 데이터베이스 초기화 프로세스를 시작합니다...")
    
    # echo=True로 설정하여 테이블 생성 과정을 터미널에 출력
    engine = create_async_engine(settings.DATABASE_URL, echo=True)
    
    try:
        async with engine.begin() as conn:
            # 1. pgvector 확장 활성화
            print("📦 pgvector 확장을 활성화하는 중...")
            await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
            
            # 2. 테이블 생성 (products, reviews)
            print("🏗️ 테이블을 생성하는 중...")
            await conn.run_sync(Base.metadata.create_all)
            
            # 3. HNSW 벡터 인덱스 생성
            print("⚡ HNSW 벡터 인덱스를 생성하는 중...")
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_review_embedding_hnsw 
                ON reviews USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64);
            """))
            
        print("✅ 모든 초기화 작업이 성공적으로 완료되었습니다!")

    except Exception as e:
        print(f"❌ 초기화 중 오류 발생: {e}", file=sys.stderr)
    finally:
        await engine.dispose()

if __name__ == "__main__":
    asyncio.run(init_db())