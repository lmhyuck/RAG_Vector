# 1. 베이스 이미지 선택 (파이썬 3.10 슬림 버전)
FROM python:3.10-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 필수 패키지 설치 (빌드 도구 포함)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. 의존성 파일 복사 및 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. 소스 코드 전체 복사
COPY . .

# 6. 포트 노출 (FastAPI 기본 포트 8000 사용 시 - 사용자의 기존 설정 준수)
EXPOSE 8000

