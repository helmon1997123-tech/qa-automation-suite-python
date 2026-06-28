import allure
import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from helpers.api_client import signup
from helpers.test_data import generate_username, generate_password


@allure.feature("UI — Авторизация")
class TestLoginUI:

    @pytest.fixture(autouse=True)
    def setup_user(self):
        self.username = generate_username()
        self.password = generate_password()
        signup(self.username, self.password)

    @allure.title("Успешный логин через UI")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "ui")
    def test_login_success(self, page: Page):
        login_page = LoginPage(page)

        with allure.step("Открываем главную страницу"):
            login_page.goto()

        with allure.step("Вводим корректные данные и логинимся"):
            login_page.login(self.username, self.password)

        with allure.step("Проверяем успешную авторизацию"):
            login_page.expect_logged_in(self.username)

    @allure.title("Логин с неверным паролем — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_login_wrong_password(self, page: Page):
        login_page = LoginPage(page)

        with allure.step("Открываем главную страницу"):
            login_page.goto()

        with allure.step("Логинимся с неверным паролем"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            login_page.login(self.username, "wrongpassword123")
            page.wait_for_timeout(2000)

        with allure.step("Проверяем ошибку"):
            assert any("Wrong password" in m for m in dialog_messages)

    @allure.title("Логин с несуществующим пользователем — ошибка")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("layer", "ui")
    def test_login_nonexistent_user(self, page: Page):
        login_page = LoginPage(page)

        with allure.step("Открываем главную страницу"):
            login_page.goto()

        with allure.step("Логинимся под несуществующим пользователем"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            login_page.login("nonexistent_xyz_123", "password123")
            page.wait_for_timeout(2000)

        with allure.step("Проверяем ошибку"):
            assert len(dialog_messages) > 0

    @allure.title("Логин с пустым username — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_login_empty_username(self, page: Page):
        login_page = LoginPage(page)

        with allure.step("Открываем главную страницу"):
            login_page.goto()

        with allure.step("Логинимся с пустым username"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            login_page.login("", self.password)
            page.wait_for_timeout(2000)

        with allure.step("Проверяем ошибку"):
            assert len(dialog_messages) > 0

    @allure.title("Логин с пустым паролем — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_login_empty_password(self, page: Page):
        login_page = LoginPage(page)

        with allure.step("Открываем главную страницу"):
            login_page.goto()

        with allure.step("Логинимся с пустым паролем"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            login_page.login(self.username, "")
            page.wait_for_timeout(2000)

        with allure.step("Проверяем ошибку"):
            assert len(dialog_messages) > 0
