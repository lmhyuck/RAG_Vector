# 1단계 : 수집 (API, Crawler)
import requests
from typing import List, Dict
import time

class BaseCollector:
    def __init__(self):
        # 실무에서는 User-Agent 설정을 통해 차단을 방지합니다.
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def fetch_raw_data(self, url: str) -> str:
        """URL로부터 로우 데이터를 가져오는 기본 메서드"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 4xx, 5xx 에러 발생 시 예외 발생
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"데이터 수집 중 오류 발생: {e}")
            return ""

    def collect(self, source_url: str) -> List[str]:
        """
        데이터 수집 실행 메서드. 
        실제 프로젝트에서는 각 사이트(네이버, 다음 등)에 맞게 
        이 메서드를 오버라이딩하거나 파싱 로직을 추가합니다.
        """
        raw_html = self.fetch_raw_data(source_url)
        
        if not raw_html:
            return []

        # 예시: 임시로 텍스트 데이터를 리스트로 반환하는 로직
        # 실제로는 BeautifulSoup이나 정규표현식으로 리뷰 본문만 추출해야 합니다.
        print(f"{source_url}에서 데이터를 성공적으로 가져왔습니다.")
        
        # 테스트용 가짜 데이터 반환 (실제 구현 시 파싱 로직으로 대체)
        return ["정말 좋은 상품이에요!", "배송이 빨라서 좋네요.", "가성비 최고입니다."]

    def sleep_between_requests(self, seconds: int = 2):
        """서버 부하 방지 및 차단 회피를 위한 대기 시간"""
        time.sleep(seconds)