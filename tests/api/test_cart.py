import allure
import pytest
from helpers.api_client import add_to_cart, get_cart
from helpers.schemas import CartItemSchema
from helpers.test_data import TestProducts
from pydantic import ValidationError


@allure.feature("Cart API")
class TestCartApi:

    @allure.title("POST /addtocart — добавление товара в корзину")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "api")
    def test_add_to_cart_success(self, auth_token):
        with allure.step("Добавляем Samsung Galaxy S6 в корзину"):
            status, _ = add_to_cart(auth_token, TestProducts.SAMSUNG_GALAXY_S6)

        with allure.step("Проверяем успешный ответ"):
            assert status == 200

    @allure.title("POST /viewcart — просмотр корзины")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "api")
    def test_view_cart_success(self, auth_token):
        with allure.step("Добавляем товар в корзину"):
            add_to_cart(auth_token, TestProducts.NOKIA_LUMIA)

        with allure.step("Запрашиваем содержимое корзины"):
            status, body = get_cart(auth_token)

        with allure.step("Проверяем статус ответа"):
            assert status == 200

        with allure.step("Валидируем схему корзины через Pydantic"):
            if body.get("Items"):
                for item in body["Items"]:
                    try:
                        CartItemSchema.model_validate(item)
                    except ValidationError as e:
                        pytest.fail(f"Cart item не прошёл валидацию: {e}")

        with allure.step("Проверяем наличие поля Items"):
            assert "Items" in body

    @allure.title("POST /addtocart — добавление нескольких товаров")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "api")
    def test_add_multiple_products(self, auth_token):
        with allure.step("Добавляем Nexus 6"):
            s1, _ = add_to_cart(auth_token, TestProducts.NEXUS_6)

        with allure.step("Добавляем iPhone 6"):
            s2, _ = add_to_cart(auth_token, TestProducts.IPHONE_6_32GB)

        with allure.step("Проверяем успешные ответы"):
            assert s1 == 200
            assert s2 == 200

    @allure.title("POST /viewcart — корзина без токена возвращает данные или пустой массив")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "api")
    def test_view_cart_without_token(self):
        with allure.step("Запрашиваем корзину без токена"):
            status, body = get_cart("")

        with allure.step("Проверяем ответ — API не возвращает ошибку"):
            assert status == 200
            assert "Items" in body

    @allure.title("POST /addtocart — добавление несуществующего товара")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("layer", "api")
    def test_add_nonexistent_product(self, auth_token):
        with allure.step("Добавляем товар с несуществующим id"):
            status, _ = add_to_cart(auth_token, 99999)

        with allure.step("Проверяем что API принимает запрос"):
            assert status == 200

    @allure.title("POST /viewcart — невалидный токен возвращает пустой массив")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("layer", "api")
    def test_view_cart_invalid_token(self):
        with allure.step("Запрашиваем корзину с невалидным токеном"):
            status, body = get_cart("invalid_token_xyz")

        with allure.step("Проверяем пустой ответ"):
            assert status == 200
            assert isinstance(body.get("Items"), list)
            assert len(body["Items"]) == 0
