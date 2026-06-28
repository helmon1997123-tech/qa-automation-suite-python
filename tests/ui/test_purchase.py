import allure
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from helpers.api_client import signup
from helpers.test_data import generate_username, generate_password, ORDER_DATA


@allure.feature("UI — Полный сценарий покупки")
class TestPurchaseUI:

    @pytest.fixture(autouse=True)
    def setup_user(self):
        self.username = generate_username()
        self.password = generate_password()
        signup(self.username, self.password)

    @allure.title("E2E: логин, выбор товара, корзина, оформление заказа")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.label("layer", "e2e")
    def test_full_purchase_flow(self, page: Page):

        with allure.step("Авторизуемся в системе"):
            login_page = LoginPage(page)
            login_page.goto()
            login_page.login(self.username, self.password)
            login_page.expect_logged_in(self.username)

        with allure.step("Выбираем товар из каталога"):
            catalog_page = CatalogPage(page)
            catalog_page.filter_by_category("phones")
            catalog_page.open_product("Samsung galaxy s6")

        with allure.step("Добавляем товар в корзину"):
            product_page = ProductPage(page)
            product_page.expect_product_loaded("Samsung galaxy s6")
            page.on("dialog", lambda d: d.accept())
            product_page.add_to_cart()
            page.wait_for_timeout(1000)

        with allure.step("Переходим в корзину"):
            catalog_page.go_to_cart()

        with allure.step("Оформляем заказ"):
            cart_page = CartPage(page)
            cart_page.expect_cart_not_empty()
            cart_page.place_order(ORDER_DATA)
            cart_page.expect_order_success()
