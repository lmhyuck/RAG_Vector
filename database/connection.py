from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 비동기 엔진 생성
engine = create_async_engine(settings.DATABASE_URL, echo=False)

# 세션 팩토리 설정
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# 상위 모델 Base 클래스 생성
# Base를 상속받은 클래스만 SQLAlchemy가 테이블로 인식
Base = declarative_base()

# DB 세션 의존성 주입용 함수
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()