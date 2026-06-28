from playwright.sync_api import Page, expect


class CatalogPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_cards = page.locator(".card-title a")
        self.cart_link = page.locator("#cartur")
        self.category_phones = page.locator("a[onclick=\"byCat('phone')\"]")
        self.category_laptops = page.locator("a[onclick=\"byCat('notebook')\"]")
        self.category_monitors = page.locator("a[onclick=\"byCat('monitor')\"]")

    def goto(self):
        self.page.goto("/")

    def filter_by_category(self, category: str):
        mapping = {
            "phones": self.category_phones,
            "laptops": self.category_laptops,
            "monitors": self.category_monitors,
        }
        mapping[category].click()
        self.page.wait_for_timeout(1500)

    def open_product(self, name: str):
        self.page.locator(".card-title a", has_text=name).first.click()
        self.page.wait_for_selector(".name", timeout=10000)

    def expect_products_visible(self):
        expect(self.product_cards.first).to_be_visible(timeout=10000)

    def go_to_cart(self):
        self.cart_link.click()
        self.page.wait_for_selector("#tbodyid", timeout=10000)
