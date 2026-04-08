import asyncio
import pandas as pd
from sqlalchemy import select
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('jhgan/ko-sroberta-multitask')

async def load_sample():
    url = "https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt"
    
    try:
        df = pd.read_csv(url, sep='\t').dropna()
        # 긍정 50개, 부정 50개 추출
        sample_data = pd.concat([df[df['label'] == 1].head(50), df[df['label'] == 0].head(50)])
    except Exception as e:
        print(f"❌ 데이터 로드 실패: {e}")
        return

    from database.connection import AsyncSessionLocal
    from database.models.product import Product
    from database.models.review import Review

    async with AsyncSessionLocal() as session:
        async with session.begin():
            # 1. 기존 상품이 있는지 확인 (중복 생성 방지)
            product_stmt = select(Product).where(Product.name == "2024 시네마 대축제 (무료 시사회)")
            result = await session.execute(product_stmt)
            movie = result.scalar_one_or_none()

            if not movie:
                movie = Product(name="2024 시네마 대축제 (무료 시사회)", category="영화/엔터테인먼트", price=0)
                session.add(movie)
                await session.flush()
                print(f"🆕 새 상품 생성: {movie.name}")
            else:
                print(f"✅ 기존 상품 활용: {movie.name}")

            # 2. 기존에 저장된 리뷰 내용들 가져오기 (중복 체크용)
            review_stmt = select(Review.content).where(Review.product_id == movie.id)
            review_result = await session.execute(review_stmt)
            existing_contents = set(review_result.scalars().all())

            # 3. 새로운 리뷰만 선별하여 추가
            reviews_to_add = []
            for _, row in sample_data.iterrows():
                content = row['document']
                
                # 이미 DB에 있는 내용이면 패스!
                if content in existing_contents:
                    continue
                
                embedding = model.encode(content).tolist()
                new_review = Review(
                    product_id=movie.id,
                    content=content,
                    embedding=embedding,
                    sentiment_score=float(row['label'])
                )
                reviews_to_add.append(new_review)
            
            if reviews_to_add:
                session.add_all(reviews_to_add)
                print(f"🔄 {len(reviews_to_add)}개의 새로운 리뷰를 추가합니다.")
            else:
                print("✨ 추가할 새로운 리뷰가 없습니다. (모두 중복)")
            
        await session.commit()

if __name__ == "__main__":
    asyncio.run(load_sample())