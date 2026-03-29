import requests
import allure
from urls import Urls
from data import generate_random_string


class TestCourierCreate:

    @allure.title('Проверка успешного создания аккаунта курьера с валидными данными.')
    @allure.description('Создание нового аккаунта курьера. Проверка кода и тела ответа')
    def test_create_courier_account(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        assert response.status_code == 201, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'ok': True}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка ошибки при повторном использовании логина для создания аккаунта курьера.')
    @allure.description('Создание нового аккаунта. Повторный запрос на создание аккаунта курьера используя такой же логин. Проверка кода и тела ответа.')
    def test_create_courier_existing_login(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        login = payload['login']

        payload_duplicate = {
            'login': login,
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }
        response_duplicate = requests.post(Urls.url_courier, data=payload_duplicate)

        assert response_duplicate.status_code == 409, f"Unexpected status code: {response_duplicate.status_code}"
        assert response_duplicate.json() == {'message': "Этот логин уже используется"}, f"Unexpected response: {response_duplicate.json()}"

    @allure.title('Проверка получения ошибки при создании аккаунта курьера с незаполненным обязательным полем - логин')
    @allure.description('Передача набора обязательных данных без логина. Проверка кода и тела ответа.')
    def test_create_courier_account_with_empty_login(self):
        no_login = {
            'login': '',
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }
        response = requests.post(Urls.url_courier, data=no_login)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для создания учетной записи'}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка получения ошибки при создании аккаунта курьера с незаполненным обязательным полем - пароль')
    @allure.description('Передача набора обязательных данных без пароля. Проверка кода и тела ответа.')
    def test_create_courier_account_with_empty_password(self):
        no_pass = {
            'login': generate_random_string(10),
            'password': '',
            'firstName': generate_random_string(10)
        }
        response = requests.post(Urls.url_courier, data=no_pass)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для создания учетной записи'}, f"Unexpected response: {response.json()}"