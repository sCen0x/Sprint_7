import requests
import allure
from urls import Urls
from data import generate_random_string


class TestCourierLogin:

    @allure.title('Проверка успешной авторизации курьера при вводе валидных данных')
    @allure.description('Создание нового аккаунта курьера. Авторизация c ним в системе. Проверка кода и тела ответа.')
    def test_courier_login_success(self, existing_courier):
        login = existing_courier['login']
        password = existing_courier['password']

        login_payload = {
            'login': login,
            'password': password
        }

        with allure.step(f'Отправить POST-запрос на авторизацию с логином: {login}'):
            response = requests.post(Urls.url_courier_login, data=login_payload)
        with allure.step('Проверить, что статус код ответа равен 200'):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"
        with allure.step('Проверить, что тело ответа содержит поле "id"'):
            response_json = response.json()
            assert 'id' in response_json, f"Response does not contain 'id'. Got: {response_json}"

    @allure.title('Проверка получения ошибки при авторизации курьера с некорректным паролем.')
    @allure.description('Создание нового аккаунта курьера. Авторизация с корректным логином и некорректным паролем. Проверка кода и тела ответа.')
    def test_courier_login_wrong_password(self, existing_courier):
        login = existing_courier['login']
        wrong_password = generate_random_string(10)

        login_payload = {
            'login': login,
            'password': wrong_password
        }
        
        with allure.step(f'Отправить POST-запрос на авторизацию с некорректным паролем: {wrong_password}'):
            response = requests.post(Urls.url_courier_login, data=login_payload)
        with allure.step('Проверить, что статус код ответа равен 404 (Not Found)'):
            assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        with allure.step('Проверить, что тело ответа содержит сообщение "Учетная запись не найдена"'):
            response_json = response.json()
            assert response_json.get('message') == 'Учетная запись не найдена', \
                f"Expected message 'Учетная запись не найдена', got: {response_json.get('message')}"


    @allure.title('Проверка получения ошибки при авторизации курьера с некорректным логином.')
    @allure.description('Создание нового аккаунта курьера. Авторизация с некорректным логином и корректным паролем. Проверка кода и тела ответа.')
    def test_courier_login_wrong_login(self, courier_data):
        password = courier_data['password']
        wrong_login = generate_random_string(10)
        
        login_payload = {
            'login': wrong_login,
            'password': password
        }
        
        with allure.step(f'Отправить POST-запрос на авторизацию с некорректным логином: {wrong_login}'):
            response = requests.post(Urls.url_courier_login, data=login_payload)
        with allure.step('Проверить, что статус код ответа равен 404 (Not Found)'):
            assert response.status_code == 404, f"Unexpected status code: {response.status_code}"
        with allure.step('Проверить, что тело ответа содержит сообщение "Учетная запись не найдена"'):
            response_json = response.json()
            assert response_json.get('message') == 'Учетная запись не найдена', \
                f"Expected message 'Учетная запись не найдена', got: {response_json.get('message')}"

    @allure.title('Проверка получения ошибки при авторизации курьера с пустым полем логин.')
    @allure.description('В тест передаётся набор данных с пустым логином. Проверка кода и тела ответа.')
    def test_courier_login_empty_login(self, courier_data):
        password = courier_data['password']
        
        login_payload = {
            'login': '',
            'password': password
        }
        
        with allure.step('Отправить POST-запрос на авторизацию с пустым логином'):
            response = requests.post(Urls.url_courier_login, data=login_payload)
        with allure.step('Проверить, что статус код ответа равен 400 (Bad Request)'):
            assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        with allure.step('Проверить, что тело ответа содержит сообщение "Недостаточно данных для входа"'):
            response_json = response.json()
            assert response_json.get('message') == 'Недостаточно данных для входа', \
                f"Expected message 'Недостаточно данных для входа', got: {response_json.get('message')}"


    @allure.title('Проверка получения ошибки при авторизации курьера с пустым полем пароль.')
    @allure.description('В тест передаётся набор данных с пустым паролем. Проверка кода и тела ответа.')
    def test_courier_login_empty_password(self, courier_data):
        login = courier_data['login']
        
        login_payload = {
            'login': login,
            'password': ''
        }
        
        with allure.step('Отправить POST-запрос на авторизацию с пустым паролем'):
            response = requests.post(Urls.url_courier_login, data=login_payload)
        with allure.step('Проверить, что статус код ответа равен 400 (Bad Request)'):
            assert response.status_code == 400, f"Unexpected status code: {response.status_code}"
        with allure.step('Проверить, что тело ответа содержит сообщение "Недостаточно данных для входа"'):
            response_json = response.json()
            assert response_json.get('message') == 'Недостаточно данных для входа', \
                f"Expected message 'Недостаточно данных для входа', got: {response_json.get('message')}"