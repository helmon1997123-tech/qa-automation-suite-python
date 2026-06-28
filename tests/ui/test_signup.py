import allure
import pytest
from playwright.sync_api import Page
from pages.signup_page import SignupPage
from helpers.api_client import signup
from helpers.test_data import generate_username, generate_password


@allure.feature("UI — Регистрация")
class TestSignupUI:

    @allure.title("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "ui")
    def test_signup_success(self, page: Page):
        signup_page = SignupPage(page)
        username = generate_username()
        password = generate_password()

        with allure.step("Открываем главную страницу"):
            signup_page.goto()

        with allure.step("Регистрируем нового пользователя"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            signup_page.signup(username, password)
            page.wait_for_timeout(2000)

        with allure.step("Проверяем сообщение об успехе"):
            assert any("Sign up successful" in m for m in dialog_messages)

    @allure.title("Регистрация с уже существующим username — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_signup_duplicate_username(self, page: Page):
        username = generate_username()
        password = generate_password()

        with allure.step("Предварительно регистрируем пользователя через API"):
            signup(username, password)

        signup_page = SignupPage(page)

        with allure.step("Открываем главную страницу"):
            signup_page.goto()

        with allure.step("Пытаемся зарегистрировать того же пользователя повторно"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            signup_page.signup(username, password)
            page.wait_for_timeout(2000)

        with allure.step("Проверяем ошибку дублирования"):
            assert any("already exist" in m for m in dialog_messages)

    @allure.title("Регистрация с пустым username — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_signup_empty_username(self, page: Page):
        signup_page = SignupPage(page)

        with allure.step("Открываем главную страницу"):
            signup_page.goto()

        with allure.step("Пытаемся зарегистрироваться с пустым username"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            signup_page.signup("", generate_password())
            page.wait_for_timeout(2000)

        with allure.step("Проверяем что появилось сообщение об ошибке"):
            assert len(dialog_messages) > 0

    @allure.title("Регистрация с пустым паролем — ошибка")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "ui")
    def test_signup_empty_password(self, page: Page):
        signup_page = SignupPage(page)

        with allure.step("Открываем главную страницу"):
            signup_page.goto()

        with allure.step("Пытаемся зарегистрироваться с пустым паролем"):
            dialog_messages = []
            page.on("dialog", lambda d: (dialog_messages.append(d.message), d.accept()))
            signup_page.signup(generate_username(), "")
            page.wait_for_timeout(2000)

        with allure.step("Проверяем что появилось сообщение об ошибке"):
            assert len(dialog_messages) > 0
