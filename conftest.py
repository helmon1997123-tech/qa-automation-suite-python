import pytest
from helpers.api_client import login, signup
from helpers.test_data import generate_password, generate_username


@pytest.fixture(scope="session")
def auth_token() -> str:
    username = generate_username()
    password = generate_password()
    signup(username, password)
    _, body = login(username, password)
    assert isinstance(body, str) and len(body) > 0, "Failed to get auth token"
    return body
