import allure
import pytest
from helpers.api_client import get_product_by_id, get_products
from helpers.schemas import ProductListSchema, ProductSchema
from helpers.test_data import TestProducts
from pydantic import ValidationError


@allure.feature("Products API")
class TestProductsApi:

    @allure.title("GET /entries — получение списка товаров")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "api")
    def test_get_products_success(self):
        with allure.step("Запрашиваем список товаров"):
            status, body = get_products()

        with allure.step("Проверяем статус ответа"):
            assert status == 200

        with allure.step("Валидируем схему ответа через Pydantic"):
            product_list = ProductListSchema.model_validate(body)

        with allure.step("Проверяем что список не пустой"):
            assert len(product_list.Items) > 0

    @allure.title("GET /entries — каждый товар содержит обязательные поля")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "api")
    def test_get_products_schema_each_item(self):
        with allure.step("Запрашиваем список товаров"):
            _, body = get_products()

        with allure.step("Валидируем схему каждого товара через Pydantic"):
            for item in body["Items"]:
                try:
                    ProductSchema.model_validate(item)
                except ValidationError as e:
                    pytest.fail(f"Товар id={item.get('id')} не прошёл валидацию: {e}")

    @allure.title("POST /view — получение товара по id")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "api")
    def test_get_product_by_id(self):
        with allure.step("Запрашиваем товар по id"):
            status, body = get_product_by_id(TestProducts.SAMSUNG_GALAXY_S6)

        with allure.step("Проверяем статус ответа"):
            assert status == 200

        with allure.step("Валидируем схему товара через Pydantic"):
            ProductSchema.model_validate(body)

    @allure.title("POST /view — товар Samsung Galaxy S6 содержит корректные данные")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "api")
    def test_get_product_data_correct(self):
        with allure.step("Запрашиваем товар Samsung Galaxy S6"):
            _, body = get_product_by_id(TestProducts.SAMSUNG_GALAXY_S6)

        with allure.step("Проверяем данные товара"):
            assert "Samsung" in body["title"]
            assert isinstance(body["price"], (int, float))
            assert body["price"] > 0

    @allure.title("POST /view — несуществующий id возвращает ошибку")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("layer", "api")
    def test_get_product_nonexistent_id(self):
        with allure.step("Запрашиваем несуществующий товар"):
            status, body = get_product_by_id(99999)

        with allure.step("Проверяем ответ"):
            assert status == 200
            assert "errorMessage" in body
