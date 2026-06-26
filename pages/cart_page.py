from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class CartPage(BasePage):
    
    CART_ITEM = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    REMOVE_BUTTON = (By.CSS_SELECTOR, "button[data-test*='remove']")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    
    def wait_for_page_to_load(self):
        """Wait for the checkout button to be visible."""
        self.wait.until(EC.visibility_of_element_located(self.CHECKOUT_BUTTON))
    
    def get_cart_items(self):
        items = self.driver.find_elements(*self.CART_ITEM)
        item_names = []
        for item in items:
            name = item.find_element(*self.ITEM_NAME).text
            item_names.append(name)
        return item_names
    
    def remove_item(self, item_name):
        items = self.driver.find_elements(*self.CART_ITEM)
        for item in items:
            name = item.find_element(*self.ITEM_NAME).text
            if name == item_name:
                remove_btn = item.find_element(*self.REMOVE_BUTTON)
                remove_btn.click()
                return True
        return False
    
    def proceed_to_checkout(self):
        """Click the checkout button."""
        self.wait_for_page_to_load()
        self.click(self.CHECKOUT_BUTTON)