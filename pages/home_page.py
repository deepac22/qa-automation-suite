from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class HomePage(BasePage):
    
    # Correct locators for SauceDemo
    WELCOME_MESSAGE = (By.CLASS_NAME, "app_logo")
    LOGOUT_BUTTON = (By.ID, "react-burger-menu-btn")
    
    def get_welcome_text(self):
        return self.get_text(self.WELCOME_MESSAGE)
    
    def is_logged_in(self):
        # Check if the menu button is visible (means logged in)
        return self.is_element_visible(self.LOGOUT_BUTTON)