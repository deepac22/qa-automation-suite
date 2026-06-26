from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    """Base class for all page objects. Contains common methods."""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def click(self, by_locator):
        """Wait for element to be clickable and click it."""
        element = self.wait.until(EC.element_to_be_clickable(by_locator))
        element.click()
    
    def enter_text(self, by_locator, text):
        """Find element and type text into it."""
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        element.clear()
        element.send_keys(text)
    
    def get_text(self, by_locator):
        """Get text from an element."""
        element = self.wait.until(EC.visibility_of_element_located(by_locator))
        return element.text
    
    def is_element_visible(self, by_locator):
        """Check if an element is visible on the page."""
        try:
            self.wait.until(EC.visibility_of_element_located(by_locator))
            return True
        except:
            return False