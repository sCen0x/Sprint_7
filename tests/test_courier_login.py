import requests
import allure
from urls import Urls
from data import generate_random_string


class TestCourierLogin:

    @allure.title('Проверка успешной авторизации курьера при вводе валидных данных')
    @allure.description('Создание нового аккаунта курьера. Авторизация c ним в системе. Проверка кода и тела ответа.')
    def test_courier_login_success(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        login = payload['login']
        password = payload['password']

        payload = {
            'login': login,
            'password': password
        }

        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        response_json = response.json()
        assert 'id' in response_json, "Response does not contain 'id'"

    @allure.title('Проверка получения ошибки при авторизации курьера с некорректным паролем.')
    @allure.description('Создание нового аккаунта курьера. Авторизация с корректным логином и некорректным паролем. Проверка кода и тела ответа.')
    def test_courier_login_wrong_password(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        login = payload['login']
        password = generate_random_string(10)

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Учетная запись не найдена'}, f"Unexpected response: {response.json()}"


    @allure.title('Проверка получения ошибки при авторизации курьера с некорректным логином.')
    @allure.description('Создание нового аккаунта курьера. Авторизация с некорректным логином и корректным паролем. Проверка кода и тела ответа.')
    def test_courier_login_wrong_login(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        login = generate_random_string(10)
        password = payload['password']

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Учетная запись не найдена'}, f"Unexpected response: {response.json()}"

    @allure.title('Проверка получения ошибки при авторизации курьера с пустым полем логин.')
    @allure.description('В тест передаётся набор данных с пустым логином. Проверка кода и тела ответа.')
    def test_courier_login_empty_login(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        login = ''
        password = payload['password']

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {
            'message': 'Недостаточно данных для входа'}, f"Unexpected response: {response.json()}"


    @allure.title('Проверка получения ошибки при авторизации курьера с пустым полем пароль.')
    @allure.description('В тест передаётся набор данных с пустым паролем. Проверка кода и тела ответа.')
    def test_courier_login_empty_password(self, register_new_courier):
        response, payload, courier_id = register_new_courier
        login = payload['login']
        password = ''

        payload = {
            'login': login,
            'password': password
        }
        response = requests.post(Urls.url_courier_login, data=payload)
        assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        assert response.json() == {'message': 'Недостаточно данных для входа'}, f"Unexpected response: {response.json()}"
