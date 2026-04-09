# 리뷰 및 벡터 데이터 테이블
from sqlalchemy import Column, Integer, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from database.connection import Base

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    content = Column(Text, nullable=False)  # 원문 리뷰
    summary = Column(Text)                  # LLM이 요약한 내용 (선택)
    
    # 벡터 저장 컬럼: 사용 모델의 차원(예: SBERT의 경우 768)에 맞게 설정
    # 벡터 검색 성능을 위해 768차원 상수로 정의
    embedding = Column(Vector(768)) 
    
    sentiment_score = Column(Float)         # 감성 분석 점수
    
    product = relationship("Product", back_populates="reviews")