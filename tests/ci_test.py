import pytest
import requests
import time

# 테스트 대상 URL
BASE_URL = "http://localhost:5001"

def test_health_check():
    """1. 서버가 살아있는지 가장 먼저 확인"""
    try:
        response = requests.get(BASE_URL)
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail(f"❌ Server is down! Cannot connect to {BASE_URL}")

def test_core_function():
    """2. Core Function 기능 테스트"""
    print("Testing Core Function...")
    response = requests.get(f"{BASE_URL}/core")
    
    # pytest의 핵심: 그냥 assert만 쓰면 됩니다!
    assert response.status_code == 200
    assert response.text == "Success"

def test_legacy_feature():
    """3. Legacy Feature 기능 테스트"""
    print("Testing Legacy Feature...")
    response = requests.get(f"{BASE_URL}/legacy")
    
    assert response.status_code == 200
    assert response.text == "Response A"

# 나중에 Feature B가 생기면 이렇게 추가만 하면 됨
# def test_feature_b():
#     resp = requests.get(...)
#     assert resp.text == "New Feature"