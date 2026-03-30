import requests
import pytest
from urls import Urls
from data import generate_random_string

@pytest.fixture
def courier_data():
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    payload = {
        'login': login,
        'password': password,
        'firstName': first_name
    }

    yield payload

    login_payload = {
        'login': login,
        'password': password
    }
    login_response = requests.post(Urls.url_courier_login, data=login_payload)
    if login_response.status_code == 200:
        courier_id = login_response.json().get('id')
        if courier_id:
            requests.delete(f"{Urls.url_courier}/{courier_id}")