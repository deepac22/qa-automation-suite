from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CheckoutPage(BasePage):
    
    # Locators
    FIRST_NAME_FIELD = (By.ID, "first-name")
    LAST_NAME_FIELD = (By.ID, "last-name")
    POSTAL_CODE_FIELD = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")
    CANCEL_BUTTON = (By.ID, "cancel")
    COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "h3[data-test='error']")
    
    def fill_checkout_info(self, first_name, last_name, postal_code):
        """Fill out the checkout information form."""
        self.enter_text(self.FIRST_NAME_FIELD, first_name)
        self.enter_text(self.LAST_NAME_FIELD, last_name)
        self.enter_text(self.POSTAL_CODE_FIELD, postal_code)
        self.click(self.CONTINUE_BUTTON)
    
    def finish_checkout(self):
        """Complete the checkout process."""
        self.click(self.FINISH_BUTTON)
    
    def get_complete_message(self):
        """Get the success message after checkout."""
        return self.get_text(self.COMPLETE_HEADER)
    
    def get_error_message(self):
        """Get error message if checkout fails."""
        return self.get_text(self.ERROR_MESSAGE)