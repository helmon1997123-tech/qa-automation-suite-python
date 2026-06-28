from playwright.sync_api import Page, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.nav_login_link = page.locator("#login2")
        self.username_input = page.locator("#loginusername")
        self.password_input = page.locator("#loginpassword")
        self.login_button = page.locator('button[onclick="logIn()"]')
        self.welcome_user = page.locator("#nameofuser")

    def goto(self):
        self.page.goto("/")

    def open_login_modal(self):
        self.nav_login_link.click()
        expect(self.username_input).to_be_visible(timeout=5000)

    def login(self, username: str, password: str):
        self.open_login_modal()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def expect_logged_in(self, username: str):
        expect(self.welcome_user).to_contain_text(f"Welcome {username}", timeout=10000)
