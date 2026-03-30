import requests
import allure
from urls import Urls
from data import generate_random_string


class TestCourierCreate:

    @allure.title('Проверка успешного создания аккаунта курьера с валидными данными.')
    @allure.description('Создание нового аккаунта курьера. Проверка кода и тела ответа')
    def test_create_courier_account(self, courier_data):
        payload = courier_data

        with allure.step(f'Отправить POST-запрос на создание курьера'):
            response = requests.post(Urls.url_courier, data=payload)
        with allure.step('Проверить, что статус код ответа равен 201'):
            assert response.status_code == 201, f"Expected 201, got {response.status_code}. Response: {response.text}"
        with allure.step('Проверить, что тело ответа содержит {"ok": True}'):
            response_json = response.json()
            assert response_json.get('ok') is True, f"Expected 'ok': True, got: {response_json}"

    @allure.title('Проверка ошибки при повторном использовании логина для создания аккаунта курьера.')
    @allure.description('Создание нового аккаунта. Повторный запрос на создание аккаунта курьера используя такой же логин. Проверка кода и тела ответа.')
    def test_create_courier_existing_login(self, courier_data):
        payload = courier_data
        login = payload['login']

        with allure.step(f'Отправить POST-запрос на создание курьера с логином: {login}'):
            response_first = requests.post(Urls.url_courier, data=payload)
        with allure.step('Проверить, что первый запрос выполнен успешно (статус 201)'):
            assert response_first.status_code == 201, \
                f"First registration failed. Status: {response_first.status_code}, Response: {response_first.text}"

        payload_duplicate = {
            'login': login,
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }
        with allure.step(f'Отправить повторный POST-запрос с тем же логином: {login}'):
            response_duplicate = requests.post(Urls.url_courier, data=payload_duplicate)
        with allure.step('Проверить, что статус код ответа равен 409 (Conflict)'):
            assert response_duplicate.status_code == 409, \
                f"Expected 409, got {response_duplicate.status_code}. Response: {response_duplicate.text}"
        with allure.step('Проверить, что тело ответа содержит правильное сообщение об ошибке'):
            response_json = response_duplicate.json()
            expected_message = "Этот логин уже используется"
            actual_message = response_json.get('message')

            assert expected_message in actual_message, \
                f"Expected message to contain '{expected_message}', got: '{actual_message}'"

    @allure.title('Проверка получения ошибки при создании аккаунта курьера с незаполненным обязательным полем - логин')
    @allure.description('Передача набора обязательных данных без логина. Проверка кода и тела ответа.')
    def test_create_courier_account_with_empty_login(self):
        no_login = {
            'login': '',
            'password': generate_random_string(10),
            'firstName': generate_random_string(10)
        }
        with allure.step('Отправить POST-запрос на создание курьера с пустым логином'):
            response = requests.post(Urls.url_courier, data=no_login)
        with allure.step('Проверить, что статус код ответа равен 400 (Bad Request)'):
            assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        with allure.step('Проверить, что тело ответа содержит сообщение об ошибке'):
            response_json = response.json()
            expected_message = "Недостаточно данных для создания учетной записи"
            actual_message = response_json.get('message')

            assert actual_message == expected_message, \
                f"Expected message '{expected_message}', got: '{actual_message}'"

    @allure.title('Проверка получения ошибки при создании аккаунта курьера с незаполненным обязательным полем - пароль')
    @allure.description('Передача набора обязательных данных без пароля. Проверка кода и тела ответа.')
    def test_create_courier_account_with_empty_password(self):
        no_pass = {
            'login': generate_random_string(10),
            'password': '',
            'firstName': generate_random_string(10)
        }
        with allure.step('Отправить POST-запрос на создание курьера с пустым паролем'):
            response = requests.post(Urls.url_courier, data=no_pass)
        with allure.step('Проверить, что статус код ответа равен 400 (Bad Request)'):
            assert response.status_code == 400, f"Expected 400, got {response.status_code}. Response: {response.text}"
        with allure.step('Проверить, что тело ответа содержит сообщение об ошибке'):
            response_json = response.json()
            expected_message = "Недостаточно данных для создания учетной записи"
            actual_message = response_json.get('message')
            
            assert actual_message == expected_message, \
                f"Expected message '{expected_message}', got: '{actual_message}'"