from playwright.sync_api import Page, expect


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.cart_items = page.locator("#tbodyid tr")
        self.place_order_button = page.locator('button[data-target="#orderModal"]')
        self.name_input = page.locator("#name")
        self.country_input = page.locator("#country")
        self.city_input = page.locator("#city")
        self.card_input = page.locator("#card")
        self.month_input = page.locator("#month")
        self.year_input = page.locator("#year")
        self.purchase_button = page.locator('button[onclick="purchaseOrder()"]')
        self.success_message = page.locator(".sweet-alert h2")

    def expect_cart_not_empty(self):
        expect(self.cart_items.first).to_be_visible(timeout=10000)

    def place_order(self, data: dict):
        self.place_order_button.click()
        expect(self.name_input).to_be_visible(timeout=5000)
        self.name_input.fill(data["name"])
        self.country_input.fill(data["country"])
        self.city_input.fill(data["city"])
        self.card_input.fill(data["card"])
        self.month_input.fill(data["month"])
        self.year_input.fill(data["year"])
        self.purchase_button.click()

    def expect_order_success(self):
        expect(self.success_message).to_contain_text("Thank you", timeout=10000)
