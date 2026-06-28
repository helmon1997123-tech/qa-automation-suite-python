from playwright.sync_api import Page, expect


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_name = page.locator(".name")
        self.add_to_cart_button = page.locator(".btn-success")

    def expect_product_loaded(self, name: str):
        expect(self.product_name).to_contain_text(name, timeout=10000)

    def add_to_cart(self):
        self.add_to_cart_button.click()
        self.page.on("dialog", lambda dialog: dialog.accept())