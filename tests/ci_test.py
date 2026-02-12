import pytest
import requests
import os

# GitHub Actions 환경변수에서 URL을 가져옵니다.
APP_URL = os.environ.get("App_URL", "http://localhost:5005")

def test_core_button():
    response = requests.get(f"{APP_URL}/core")
    assert response.status_code == 200
    assert "Success" in response.text

def test_legacy_button():
    response = requests.get(f"{APP_URL}/")
    assert response.status_code == 200
    assert "Legacy" in response.text 

def test_new_feature_response():
    response = requests.get(f"{APP_URL}/new-feature")
    assert response.status_code == 200
    assert response.text == "Response B"