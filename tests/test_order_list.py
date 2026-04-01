import requests
import allure
from data import OrderHelper
from urls import Urls

class TestOrdersListGet:

    @allure.title('Проверка получения списка заказов.')
    @allure.description('Создание четырех заказов из предопределенных данных. Запрос списка заказов. Проверка кода и тела ответа.')
    def test_orders_get_list(self):

        order_data_list = OrderHelper.get_predefined_order_data()
        with allure.step(f'Создать 4 заказа с разными параметрами цвета'):
            add_new_orders = OrderHelper.create_orders(order_data_list)
        with allure.step('Отправить GET-запрос на получение списка заказов'):
            response = requests.get(Urls.url_orders_create)
        with allure.step('Проверить, что статус код ответа равен 200'):
            assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"
        with allure.step('Проверить, что тело ответа содержит поле "orders" в виде списка'):
            response_json = response.json()
            assert isinstance(response_json.get('orders'), list), f"'orders' is not a list. Response: {response_json}"
