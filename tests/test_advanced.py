import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage

class TestAdvanced:
    
    @pytest.fixture(autouse=True)
    def setup(self):
        """Reset cart by navigating to a fresh session."""
        # This runs before each test
        pass
    
    @pytest.fixture
    def driver(self):
        """Create a fresh WebDriver session for each test."""
        chrome_options = Options()
        if os.getenv("CI") == "true":
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--window-size=1920,1080")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.maximize_window()
        driver.get("https://www.saucedemo.com/")
        
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        
        yield driver
        driver.quit()
    
    def test_cart_is_empty_on_load(self, driver):
        """Verify cart is empty when first landing on the products page."""
        products_page = ProductsPage(driver)
        cart_count = products_page.get_cart_count()
        assert cart_count == 0, "Cart should be empty when no items added"
    
    def test_checkout_with_empty_cart(self, driver):
        """Verify that the user can proceed to checkout with an empty cart."""
        products_page = ProductsPage(driver)
        products_page.go_to_cart()
        
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        
        assert "checkout" in driver.current_url, "Should navigate to checkout page"