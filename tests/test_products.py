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

class TestProducts:
    
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
        
        # Login first
        login_page = LoginPage(driver)
        login_page.login("standard_user", "secret_sauce")
        
        yield driver
        driver.quit()
    
    def test_product_sort_by_price_low_to_high(self, driver):
        products_page = ProductsPage(driver)
        products_page.sort_by("Price (low to high)")
        prices = products_page.get_product_prices()
        assert prices == sorted(prices), "Prices should be sorted low to high"
    
    def test_product_sort_by_price_high_to_low(self, driver):
        products_page = ProductsPage(driver)
        products_page.sort_by("Price (high to low)")
        prices = products_page.get_product_prices()
        assert prices == sorted(prices, reverse=True), "Prices should be sorted high to low"
    
    def test_add_product_to_cart(self, driver):
        products_page = ProductsPage(driver)
        products_page.add_product_to_cart("Sauce Labs Backpack")
        cart_count = products_page.get_cart_count()
        assert cart_count == 1, "Cart should have 1 item"