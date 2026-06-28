import base64
import os
import time
from typing import Any

import httpx
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "https://api.demoblaze.com")


def _encode_password(password: str) -> str:
    return base64.b64encode(password.encode()).decode()


def signup(username: str, password: str) -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/signup",
            json={"username": username, "password": _encode_password(password)},
        )
        return response.status_code, response.json()


def login(username: str, password: str) -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/login",
            json={"username": username, "password": _encode_password(password)},
        )
        return response.status_code, response.json()


def get_products() -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.get(f"{API_URL}/entries")
        return response.status_code, response.json()


def get_product_by_id(product_id: int) -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/view",
            json={"id": str(product_id)},
        )
        return response.status_code, response.json()


def add_to_cart(token: str, product_id: int) -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/addtocart",
            json={
                "cookie": token,
                "flag": False,
                "id": str(int(time.time() * 1000)),
                "prod_id": product_id,
            },
        )
        body = response.json() if response.content else None
        return response.status_code, body


def get_cart(token: str) -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/viewcart",
            json={"cookie": token, "flag": False},
        )
        return response.status_code, response.json()


def place_order(
    token: str,
    name: str,
    country: str,
    city: str,
    card: str,
    month: str,
    year: str,
) -> tuple[int, Any]:
    with httpx.Client() as client:
        response = client.post(
            f"{API_URL}/order",
            json={
                "cookie": token,
                "name": name,
                "country": country,
                "city": city,
                "card": card,
                "month": month,
                "year": year,
            },
        )
        return response.status_code, response.json()
