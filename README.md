# 🔍 Review-Sense: Semantic Search Engine

이 프로젝트는 **FastAPI**와 **pgvector(PostgreSQL)**를 활용하여 대규모 리뷰 데이터를 벡터화하고, 사용자 질의에 대해 의미론적(Semantic) 검색 결과를 제공하는 검색 엔진 서비스입니다.

---

## 🛠️ Tech Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL (pgvector extension)
- **AI Model:** HuggingFace Sentence-Transformers (`jhgan/ko-sroberta-multitask`)
- **Infrastructure:** Docker, Docker Compose

---

## 🚀 Getting Started

### 1. 로컬 환경 설정 (Local Setup)
로컬 가상환경에서 코드를 실행하거나 라이브러리를 설치하려면 아래 명령어를 사용합니다.

```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 패키지 설치
pip install -r requirements.txt

# 서비스 빌드 및 백그라운드 실행
docker-compose up -d --build

# (최초 실행 시) 데이터베이스 스키마 생성 및 샘플 데이터 로드
docker exec -it review_api python -m scripts.load_sample_data
