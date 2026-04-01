import requests
import pytest
from urls import Urls
from data import generate_random_string

@pytest.fixture
def courier_data():
    return {
    "login": generate_random_string(10),
    "password": generate_random_string(10),
    "firstName": generate_random_string(10)
    }

@pytest.fixture
def existing_courier(courier_data):
    
    response = requests.post(Urls.url_courier, data=courier_data)
    if response.status_code != 201:
        pytest.skip(
            f"Failed to create courier for test."
            f"Статус:{response.status_code}, Ответ: {response.text}")
    
    yield courier_data
    try:
        login_response = requests.post(Urls.url_courier_login, data={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')
            if courier_id:
                requests.delete(f"{Urls.url_courier}/{courier_id}")
    except Exception:
        pass            