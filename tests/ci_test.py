import pytest
import requests
import os

'''
During CI, it will not use the APP_URL value defined here.
It will be replaced with http://app-test:5000 in docker network
'''

APP_URL = os.environ.get("App_URL", "URL_TO_BE_REPLACED")

def test_core_button():
    response = requests.get(f"{APP_URL}/core")
    assert response.status_code == 200
    assert "Success" in response.text

def test_legacy_button():
    response = requests.get(f"{APP_URL}/")
    assert response.status_code == 200
    assert "Legacy" in response.text 

# def test_new_feature_response():
#     response = requests.get(f"{APP_URL}/new-feature")
#     assert response.status_code == 200
#     assert response.text == "Response B"