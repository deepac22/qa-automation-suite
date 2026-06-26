from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage

class ProductsPage(BasePage):
    
    # Locators
    PRODUCT_ITEM = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAME = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICE = (By.CLASS_NAME, "inventory_item_price")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[data-test*='add-to-cart']")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-test*='remove']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    SHOPPING_CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    def get_product_names(self):
        """Get list of all product names on the page."""
        elements = self.driver.find_elements(*self.PRODUCT_NAME)
        return [elem.text for elem in elements]
    
    def get_product_prices(self):
        """Get list of all product prices on the page."""
        elements = self.driver.find_elements(*self.PRODUCT_PRICE)
        return [float(elem.text.replace('$', '')) for elem in elements]
    
    def add_product_to_cart(self, product_name):
        """Add a specific product to cart by name."""
        products = self.driver.find_elements(*self.PRODUCT_ITEM)
        for product in products:
            name = product.find_element(*self.PRODUCT_NAME).text
            if name == product_name:
                add_button = product.find_element(*self.ADD_TO_CART_BUTTON)
                add_button.click()
                return True
        return False
    
    def get_cart_count(self):
        """Get the number of items in cart."""
        if self.is_element_visible(self.CART_BADGE):
            return int(self.get_text(self.CART_BADGE))
        return 0
    
    def go_to_cart(self):
        """Navigate to the shopping cart."""
        self.click(self.SHOPPING_CART_LINK)
    
    def sort_by(self, sort_option):
        """Sort products by given option."""
        select = Select(self.driver.find_element(*self.SORT_DROPDOWN))
        select.select_by_visible_text(sort_option)