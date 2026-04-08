from fastapi import APIRouter
from .search import router as search_router

# 여러 라우터를 하나로 묶어서 main.py에서 한 번에 등록하기 쉽게 만듭니다.
router = APIRouter()
router.include_router(search_router)