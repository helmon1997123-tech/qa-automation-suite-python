import allure
from playwright.sync_api import Page, expect
from pages.catalog_page import CatalogPage


@allure.feature("UI — Каталог товаров")
class TestCatalogUI:

    @allure.title("Главная страница загружается и показывает товары")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "ui")
    def test_products_visible(self, page: Page):
        catalog_page = CatalogPage(page)

        with allure.step("Открываем главную страницу"):
            catalog_page.goto()

        with allure.step("Проверяем что товары отображаются"):
            catalog_page.expect_products_visible()

    @allure.title("Фильтр по категории Phones")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_filter_phones(self, page: Page):
        catalog_page = CatalogPage(page)

        with allure.step("Открываем главную страницу"):
            catalog_page.goto()
            catalog_page.expect_products_visible()

        with allure.step("Фильтруем по категории Phones"):
            catalog_page.filter_by_category("phones")
            catalog_page.expect_products_visible()

    @allure.title("Фильтр по категории Laptops")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_filter_laptops(self, page: Page):
        catalog_page = CatalogPage(page)

        with allure.step("Открываем главную страницу"):
            catalog_page.goto()
            catalog_page.expect_products_visible()

        with allure.step("Фильтруем по категории Laptops"):
            catalog_page.filter_by_category("laptops")
            catalog_page.expect_products_visible()

    @allure.title("Фильтр по категории Monitors")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_filter_monitors(self, page: Page):
        catalog_page = CatalogPage(page)

        with allure.step("Открываем главную страницу"):
            catalog_page.goto()
            catalog_page.expect_products_visible()

        with allure.step("Фильтруем по категории Monitors"):
            catalog_page.filter_by_category("monitors")
            catalog_page.expect_products_visible()

    @allure.title("Открытие карточки товара")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_open_product_card(self, page: Page):
        catalog_page = CatalogPage(page)

        with allure.step("Открываем главную страницу и фильтруем по Phones"):
            catalog_page.goto()
            catalog_page.expect_products_visible()
            catalog_page.filter_by_category("phones")

        with allure.step("Открываем карточку Samsung galaxy s6"):
            catalog_page.open_product("Samsung galaxy s6")
            expect(page.locator(".name")).to_be_visible(timeout=10000)
