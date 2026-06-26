import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class TestCheckout:
    
    @pytest.fixture
    def driver(self):
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
    
    def test_complete_checkout_flow(self, driver):
        products_page = ProductsPage(driver)
        products_page.add_product_to_cart("Sauce Labs Backpack")
        products_page.go_to_cart()
        
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info("John", "Doe", "M5V2H1")
        checkout_page.finish_checkout()
        
        success_message = checkout_page.get_complete_message()
        assert "Thank you" in success_message, "Checkout should be successful"
    
    def test_checkout_with_invalid_postal_code(self, driver):
        products_page = ProductsPage(driver)
        products_page.add_product_to_cart("Sauce Labs Backpack")
        products_page.go_to_cart()
        
        cart_page = CartPage(driver)
        cart_page.proceed_to_checkout()
        
        checkout_page = CheckoutPage(driver)
        checkout_page.fill_checkout_info("John", "Doe", "")
        
        error = checkout_page.get_error_message()
        assert "Postal Code is required" in error, "Error should be shown for missing postal code"