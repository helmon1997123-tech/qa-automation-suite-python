from playwright.sync_api import Page, expect


class SignupPage:
    def __init__(self, page: Page):
        self.page = page
        self.nav_signup_link = page.locator("#signin2")
        self.username_input = page.locator("#sign-username")
        self.password_input = page.locator("#sign-password")
        self.signup_button = page.locator('button[onclick="register()"]')

    def goto(self):
        self.page.goto("/")

    def open_signup_modal(self):
        self.nav_signup_link.click()
        expect(self.username_input).to_be_visible(timeout=5000)

    def signup(self, username: str, password: str):
        self.open_signup_modal()
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.signup_button.click()
