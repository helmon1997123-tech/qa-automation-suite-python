import allure
import pytest
from helpers.api_client import login, signup
from helpers.test_data import generate_password, generate_username


@allure.feature("Auth API")
class TestAuthApi:

    @allure.title("POST /signup — успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "api")
    def test_signup_success(self):
        username = generate_username()
        password = generate_password()

        with allure.step("Регистрируем нового пользователя"):
            status, body = signup(username, password)

        with allure.step("Проверяем успешный ответ"):
            assert status == 200
            assert "errorMessage" not in body

    @allure.title("POST /signup — регистрация с уже существующим username")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "api")
    def test_signup_duplicate_username(self):
        username = generate_username()
        password = generate_password()

        with allure.step("Регистрируем пользователя первый раз"):
            signup(username, password)

        with allure.step("Пытаемся зарегистрировать того же пользователя повторно"):
            _, body = signup(username, password)

        with allure.step("Проверяем ошибку дублирования"):
            assert "errorMessage" in body
            assert "already exist" in body["errorMessage"]

    @allure.title("POST /login — успешный логин")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("layer", "api")
    def test_login_success(self):
        username = generate_username()
        password = generate_password()

        with allure.step("Предварительно регистрируем пользователя"):
            signup(username, password)

        with allure.step("Выполняем логин"):
            status, body = login(username, password)

        with allure.step("Проверяем успешный ответ с токеном"):
            assert status == 200
            assert isinstance(body, str)
            assert len(body) > 0

    @allure.title("POST /login — неверный пароль")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.label("layer", "api")
    def test_login_wrong_password(self):
        username = generate_username()
        password = generate_password()

        with allure.step("Регистрируем пользователя"):
            signup(username, password)

        with allure.step("Логинимся с неверным паролем"):
            _, body = login(username, "wrongpassword")

        with allure.step("Проверяем ошибку авторизации"):
            assert "errorMessage" in body

    @allure.title("POST /login — несуществующий пользователь")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("layer", "api")
    def test_login_nonexistent_user(self):
        with allure.step("Логинимся под несуществующим пользователем"):
            _, body = login("nonexistent_user_xyz_123", "password123")

        with allure.step("Проверяем ошибку"):
            assert "errorMessage" in body
