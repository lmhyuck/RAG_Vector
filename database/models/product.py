# 상품 정보 테이블
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database.connection import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True) # 상품명 검색 대비 인덱스
    category = Column(String(100), index=True)
    price = Column(Integer)
    brand = Column(String(100))
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 1:N 관계 설정 (하나의 상품은 여러 개의 리뷰를 가짐)
    reviews = relationship("Review", back_populates="product", cascade="all, delete-orphan")