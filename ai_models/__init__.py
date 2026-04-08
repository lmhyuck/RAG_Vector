from .embedder import Embedder
from .llm_analyzer import LLMAnalyzer

# 싱글톤 패턴: 모델을 미리 인스턴스화해두고 어디서든 공유해서 사용
# 이렇게 하면 API 서버가 뜰 때 딱 한 번만 모델을 메모리에 올립니다.
embedder = Embedder()
llm_analyzer = LLMAnalyzer()

# 외부에서 'from ai_models import embedder' 형태로 바로 사용할 수 있게 노출
__all__ = ["embedder", "llm_analyzer", "Embedder", "LLMAnalyzer"]