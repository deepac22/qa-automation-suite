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

class TestAdvanced:
    
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
    
    def test_cart_is_empty_on_load(self, driver):
        products_page = ProductsPage(driver)
        cart_count = products_page.get_cart_count()
        assert cart_count == 0, "Cart should be empty when no items added"
    
    def test_checkout_with_empty_cart(self, driver):
        products_page = ProductsPage(driver)
        products_page.go_to_cart()
        
        cart_page = CartPage(driver)
        
        # SauceDemo does NOT allow checkout with empty cart
        current_url_before = driver.current_url
        cart_page.proceed_to_checkout()
        current_url_after = driver.current_url
        
        # User should stay on the cart page
        assert current_url_before == current_url_after, "User should not proceed to checkout with empty cart"