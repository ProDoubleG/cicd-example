import pytest
import requests
import os # 환경변수 읽기 위해 추가

# [수정] 환경변수에서 주소를 읽어오거나, 없으면 localhost 사용 (로컬 테스트용)
# 도커 내부 통신일 때는 'http://app-test:5000'을 쓰게 됩니다.
BASE_URL = os.getenv("App_URL", "http://localhost:5001")

def test_health_check():
    # ... (나머지 코드는 동일) ...
    try:
        response = requests.get(BASE_URL)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail(f"❌ Server is down! Cannot connect to {BASE_URL}")

def test_core_function():
    # ... (나머지 코드는 동일) ...
    response = requests.get(f"{BASE_URL}/core")
    assert response.status_code == 200
    assert response.text == "Success"

def test_legacy_feature():
    # ... (나머지 코드는 동일) ...
    response = requests.get(f"{BASE_URL}/legacy")
    assert response.status_code == 200
    assert response.text == "Response A"