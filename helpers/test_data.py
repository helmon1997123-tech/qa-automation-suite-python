import time


def generate_username() -> str:
    return f"testuser_{int(time.time() * 1000) % 10**9}"


def generate_password() -> str:
    return f"Pass_{int(time.time() * 1000) % 10**9}"


class TestProducts:
    SAMSUNG_GALAXY_S6 = 1
    NOKIA_LUMIA = 2
    NEXUS_6 = 3
    SAMSUNG_GALAXY_S7 = 4
    IPHONE_6_32GB = 5
    SONY_VAIO_I5 = 6


ORDER_DATA = {
    "name": "Test User",
    "country": "Russia",
    "city": "Moscow",
    "card": "4111111111111111",
    "month": "12",
    "year": "2026",
}
