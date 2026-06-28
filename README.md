# QA Automation Suite — Python

[![CI](https://github.com/helmon1997123-tech/qa-automation-suite-python/actions/workflows/tests.yml/badge.svg)](https://github.com/helmon1997123-tech/qa-automation-suite-python/actions/workflows/tests.yml)
API + UI тест-фреймворк для [Demoblaze](https://www.demoblaze.com) на Python.

## Стек

| Инструмент       | Назначение                         |
|------------------|------------------------------------|
| Python 3.12      | Язык разработки                    |
| pytest           | Тест-раннер                        |
| httpx            | HTTP-клиент                        |
| Pydantic v2      | Валидация схем API-ответов (≈ Zod) |
| pytest-playwright| UI автотесты                       |
| allure-pytest    | Отчёты с шагами и severity         |
| pytest-xdist     | Параллельный запуск (`-n auto`)    |
| GitHub Actions   | CI/CD пайплайн                     |
| Telegram Bot     | Нотификации о результатах          |

## Структура

qa-automation-suite-python/

├── tests/

│   ├── api/

│   │   ├── test_auth.py       # POST /signup, POST /login

│   │   ├── test_products.py   # GET /entries, POST /view

│   │   └── test_cart.py       # POST /addtocart, POST /viewcart

│   └── ui/

│       ├── test_signup.py     # Регистрация через UI

│       ├── test_login.py      # Авторизация через UI

│       ├── test_catalog.py    # Каталог и фильтрация

│       └── test_purchase.py   # E2E: логин → товар → корзина → заказ

├── pages/                     # Page Object Model

│   ├── signup_page.py

│   ├── login_page.py

│   ├── catalog_page.py

│   ├── product_page.py

│   └── cart_page.py

├── helpers/

│   ├── api_client.py          # HTTP-клиент (httpx)

│   ├── schemas.py             # Pydantic-схемы (аналог Zod)

│   └── test_data.py           # Генераторы данных и константы

├── conftest.py                # Фикстуры pytest (auth_token)

├── pytest.ini                 # Конфигурация pytest + allure

├── run.sh                     # Запуск всех тестов + отчёт

├── run_api.sh                 # Запуск API тестов + отчёт

├── run_ui.sh                  # Запуск UI тестов + отчёт

├── requirements.txt

└── .env.example

## Покрытие

### API тесты (16)

| Тест | Severity |
|------|----------|
| POST /signup — успешная регистрация | Critical |
| POST /signup — дублирующий username | Normal |
| POST /login — успешный логин | Critical |
| POST /login — неверный пароль | Normal |
| POST /login — несуществующий пользователь | Minor |
| GET /entries — список товаров + Pydantic валидация | Critical |
| GET /entries — валидация схемы каждого товара | Normal |
| POST /view — товар по id + Pydantic валидация | Critical |
| POST /view — корректные данные товара | Normal |
| POST /view — несуществующий id | Minor |
| POST /addtocart — добавление товара | Critical |
| POST /viewcart — просмотр корзины + Pydantic валидация | Critical |
| POST /addtocart — несколько товаров | Normal |
| POST /viewcart — без токена | Normal |
| POST /addtocart — несуществующий товар | Minor |
| POST /viewcart — невалидный токен | Minor |

### UI тесты (15)

| Тест | Severity |
|------|----------|
| Регистрация — успех | Critical |
| Регистрация — дублирующий username | Normal |
| Регистрация — пустой username | Normal |
| Регистрация — пустой пароль | Normal |
| Логин — успех | Critical |
| Логин — неверный пароль | Normal |
| Логин — несуществующий пользователь | Minor |
| Логин — пустой username | Normal |
| Логин — пустой пароль | Normal |
| Каталог — товары отображаются | Critical |
| Каталог — фильтр Phones | Normal |
| Каталог — фильтр Laptops | Normal |
| Каталог — фильтр Monitors | Normal |
| Каталог — открытие карточки товара | Normal |
| E2E — логин → товар → корзина → заказ | Blocker |

## Запуск

```bash
# Установка
pip install -r requirements.txt
playwright install chromium

# UI тесты с браузером (видно выполнение)
pytest tests/ui --headed

# Все тесты + отчёт
./run.sh

# Только API + отчёт
./run_api.sh

# Только UI + отчёт
./run_ui.sh

# Allure отчёт вручную
allure serve allure-results
```

## Secrets для GitHub Actions

| Variable             | Описание                |
|----------------------|-------------------------|
| `TELEGRAM_BOT_TOKEN` | Токен Telegram бота     |
| `TELEGRAM_CHAT_ID`   | ID чата для нотификаций |
| `API_URL`            | URL API (опционально)   |